CREATE TABLE transaction_category (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for category',
    name VARCHAR(50) NOT NULL COMMENT 'Name of the category (e.g., Transfer, Payment)',
    description VARCHAR(255) COMMENT 'Detailed description of the transaction category'
);


CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for user',
    name VARCHAR(100) NOT NULL COMMENT 'Full name of the user',
    phone_number VARCHAR(20) NOT NULL UNIQUE COMMENT 'Mobile number used for MoMo',
    account_type ENUM('STANDARD', 'MERCHANT', 'AGENT') DEFAULT 'STANDARD' COMMENT 'Type of MoMo account',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp'
);


CREATE TABLE transaction (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Internal transaction ID',
    reference_id VARCHAR(50) NOT NULL UNIQUE COMMENT 'External MoMo reference ID from SMS',
    category_id INT COMMENT 'Foreign key linking to transaction_category',
    amount DECIMAL(15, 2) NOT NULL CHECK (amount > 0) COMMENT 'Transaction amount (Must be positive)',
    fee DECIMAL(15, 2) DEFAULT 0.00 CHECK (fee >= 0) COMMENT 'Transaction fee applied',
    status ENUM('PENDING', 'SUCCESS', 'FAILED') DEFAULT 'SUCCESS' COMMENT 'Current status of transaction',
    raw_sms_text TEXT COMMENT 'Original raw SMS message string',
    timestamp DATETIME NOT NULL COMMENT 'Time the transaction occurred according to SMS',
    FOREIGN KEY (category_id) REFERENCES transaction_category(id) ON DELETE SET NULL
);


CREATE TABLE user_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique record ID',
    user_id INT NOT NULL COMMENT 'Foreign key to user table',
    transaction_id INT NOT NULL COMMENT 'Foreign key to transaction table',
    role ENUM('SENDER', 'RECEIVER') NOT NULL COMMENT 'Role of the user in this specific transaction',
    balance_after DECIMAL(15, 2) COMMENT 'Account balance after transaction completed',
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES transaction(id) ON DELETE CASCADE,
    UNIQUE(user_id, transaction_id, role) 
);


CREATE TABLE system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique Log ID',
    transaction_id INT COMMENT 'Associated transaction, if applicable',
    message TEXT NOT NULL COMMENT 'Log message or error description',
    source VARCHAR(50) COMMENT 'System component generating log',
    log_type ENUM('INFO', 'WARNING', 'ERROR') DEFAULT 'INFO' COMMENT 'Severity level of the log',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Time the log was generated',
    FOREIGN KEY (transaction_id) REFERENCES transaction(id) ON DELETE CASCADE
);


CREATE INDEX idx_user_phone ON user(phone_number);
CREATE INDEX idx_transaction_ref ON transaction(reference_id);
CREATE INDEX idx_transaction_date ON transaction(timestamp);

INSERT INTO transaction_category (name, description) VALUES 
('P2P Transfer', 'Person to person money transfer'),
('Airtime Purchase', 'Buying mobile airtime'),
('Merchant Payment', 'Payment for goods or services using MoMo Pay'),
('Cash In', 'Depositing money into MoMo account at an agent'),
('Cash Out', 'Withdrawing money from MoMo account at an agent');




INSERT INTO user (name, phone_number, account_type, created_at) VALUES 
('Orla ISHIMWE', '0781234567', 'STANDARD', '2025-03-12 08:22:00'),
('Benito KABALI', '0787654321', 'STANDARD', '2025-07-19 14:05:00'),
('Kigali Supermarket', '0789998888', 'MERCHANT', '2025-11-04 09:30:00'),
('MoMo Agent 001', '0780001111', 'AGENT', '2026-01-08 07:00:00'),
('Charlie HABYARIMANA', '0785554444', 'STANDARD', '2026-04-23 16:45:00');



INSERT INTO transaction (reference_id, category_id, amount, fee, status, raw_sms_text, timestamp) VALUES 
('TXN10001', 1, 5000.00, 100.00, 'SUCCESS', 'You have transferred 5000 RWF to Benito KABALI...', '2025-04-10 08:30:00'),
('TXN10002', 3, 12500.00, 0.00, 'SUCCESS', 'Payment of 12500 RWF to Kigali Supermarket successful...', '2025-07-22 09:15:00'),
('TXN10003', 2, 1000.00, 0.00, 'SUCCESS', 'You have bought 1000 RWF airtime...', '2025-09-05 10:00:00'),
('TXN10004', 4, 50000.00, 0.00, 'SUCCESS', 'Cash in of 50000 RWF from Agent 001...', '2026-01-14 11:20:00'),
('TXN10005', 1, 15000.00, 300.00, 'FAILED', 'Transfer failed due to insufficient funds.', '2026-03-30 12:05:00');

INSERT INTO user_transactions (user_id, transaction_id, role, balance_after) VALUES 
(1, 1, 'SENDER', 14900.00),  -- Orla sent TXN1
(2, 1, 'RECEIVER', 25000.00), -- Benito received TXN1
(1, 2, 'SENDER', 2400.00),   -- Orla paid Merchant TXN2
(3, 2, 'RECEIVER', 150000.00),-- Merchant received TXN2
(5, 4, 'RECEIVER', 52000.00); -- Charlie received Cash In TXN4


INSERT INTO system_logs (transaction_id, message, source, log_type) VALUES 
(1, 'Successfully parsed P2P transfer SMS', 'ETL_Parser', 'INFO'),
(2, 'Successfully parsed Merchant Payment SMS', 'ETL_Parser', 'INFO'),
(NULL, 'Database connection timeout recovered', 'Database_Manager', 'WARNING'),
(4, 'Cash In SMS normalized successfully', 'ETL_Cleaner', 'INFO'),
(5, 'Transaction marked as failed: insufficient funds text detected', 'ETL_Categorizer', 'ERROR');