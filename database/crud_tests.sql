-- some CRUD Operations Test Queries

/* Since we have already added data in the sql database with database_setup, 
we will proceed with READ, UPDATE and DELETE queries */  

--READ

-- Reading All transactions with their category names
SELECT t.reference_id, t.amount, t.fee, t.status, t.timestamp,
       tc.name AS category
FROM transaction t
JOIN transaction_category tc ON t.category_id = tc.id;

-- Full transaction details with sender and receiver info
SELECT t.reference_id, t.amount, t.status,
       u.name AS participant, u.phone_number,
       ut.role, ut.balance_after
FROM transaction t
JOIN user_transactions ut ON t.id = ut.transaction_id
JOIN user u ON ut.user_id = u.id
ORDER BY t.reference_id, ut.role;


-- UPDATE

-- Mark a failed transaction as successful after retry
UPDATE transaction
SET status = 'SUCCESS'
WHERE reference_id = 'TXN10005';

-- Update user account type to MERCHANT
UPDATE user
SET account_type = 'MERCHANT'
WHERE phone_number = '0785554444';


-- DELETE

-- Remove a specific log entry
DELETE FROM system_logs
WHERE transaction_id = 5 AND source = 'ETL_Categorizer';

-- Remove a user-transaction link
DELETE FROM user_transactions
WHERE user_id = 5 AND transaction_id = 4;


/* SECURITY & UNIQUENESS RULES
   These should all fail with errors, proving the constraints work */

-- CHECK: reject negative amount
INSERT INTO transaction (reference_id, category_id, amount, fee, status, raw_sms_text, timestamp)
VALUES ('TXN99999', 1, -500.00, 0.00, 'SUCCESS', 'Test negative amount', '2026-05-18 10:00:00');

-- CHECK: reject negative fee
INSERT INTO transaction (reference_id, category_id, amount, fee, status, raw_sms_text, timestamp)
VALUES ('TXN99998', 1, 5000.00, -100.00, 'SUCCESS', 'Test negative fee', '2026-05-18 10:00:00');

-- UNIQUE: duplicate phone number
INSERT INTO user (name, phone_number, account_type)
VALUES ('Duplicate User', '0781234567', 'STANDARD');

-- UNIQUE: duplicate reference_id
INSERT INTO transaction (reference_id, category_id, amount, fee, status, raw_sms_text, timestamp)
VALUES ('TXN10001', 1, 3000.00, 50.00, 'SUCCESS', 'Duplicate ref test', '2026-05-18 10:00:00');

-- UNIQUE: duplicate user role per transaction
INSERT INTO user_transactions (user_id, transaction_id, role, balance_after)
VALUES (1, 1, 'SENDER', 10000.00);

-- FOREIGN KEY: invalid category_id
INSERT INTO transaction (reference_id, category_id, amount, fee, status, raw_sms_text, timestamp)
VALUES ('TXN99997', 999, 5000.00, 0.00, 'SUCCESS', 'Invalid FK test', '2026-05-18 10:00:00');
