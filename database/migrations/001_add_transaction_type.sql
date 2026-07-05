USE finance_managerDB;

ALTER TABLE transactions
ADD COLUMN transaction_type ENUM('income', 'expense') NOT NULL DEFAULT 'income';

AFTER amount;