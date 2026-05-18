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