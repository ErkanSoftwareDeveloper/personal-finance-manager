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
    transactions (user_id, amount, category)
VALUES (1, 500, 'Bank'),
    (2, 750, 'IT');

SELECT * FROM transactions;