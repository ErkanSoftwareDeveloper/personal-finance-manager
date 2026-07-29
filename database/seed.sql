USE finance_managerDB;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE users;

TRUNCATE TABLE transactions;

SET FOREIGN_KEY_CHECKS = 1;

-- Test Users
INSERT INTO
    users (username, password_hash)
VALUES ('erkan', 'fakeErkan01'),
    ('Roland', 'Felos');

SELECT * FROM users;

-- Test Transactions
INSERT INTO
    transactions (
        user_id,
        amount,
        transaction_type,
        category
    )
VALUES (1, 500, 'income', 'Bank'),
    (2, 750, 'expense', 'IT');

SELECT * FROM users;

SELECT * FROM transactions;