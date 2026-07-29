# Personal Finance Manager API

A secure REST API for managing personal income and expenses.

The application allows users to register, log in, create income and expense transactions, view their transaction history, and calculate their current balance.

## Features

* User registration
* Secure password hashing with bcrypt
* Duplicate username validation
* OAuth2-compatible login
* JWT authentication
* Authenticated user profile with `/me`
* Add income and expense transactions
* View the authenticated user's transactions
* Calculate the authenticated user's balance
* Interactive API documentation with Swagger UI

## Tech Stack

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* MySQL
* PyMySQL
* Pydantic
* Pydantic Settings
* Passlib and bcrypt
* JSON Web Tokens with python-jose

## Project Structure

```text
personal-finance-manager/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── crud.py
│   │   └── database.py
│   ├── models/
│   │   ├── transaction_model.py
│   │   └── user_model.py
│   ├── schemas/
│   │   ├── transaction_schema.py
│   │   └── user_schema.py
│   └── main.py
├── database/
│   ├── migrations/
│   ├── schema.sql
│   └── seed.sql
├── tests/
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/ErkanSoftwareDeveloper/personal-finance-manager.git
cd personal-finance-manager
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

The project uses MySQL.

Create the database and tables by running:

```text
database/schema.sql
```

You can execute this file using DBeaver, MySQL Workbench, or the MySQL command-line client.

The default database name is:

```text
finance_managerDB
```

The database connection is configured through the `DATABASE_URL` environment variable.

Do not store database credentials directly in the Python source code.

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secure-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/finance_managerDB
```

When the local MySQL root user has no password, the database URL can look like this:

```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/finance_managerDB
```

Generate a secure JWT secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value into `SECRET_KEY`.

The `.env` file is ignored by Git and must never be committed.

## Running the Application

Start the development server:

```bash
python -m uvicorn app.main:app --reload
```

If the `python` command is not available, use:

```bash
python3 -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Authentication Flow

1. Register a new user with `POST /register`.
2. Log in with `POST /login`.
3. The API returns a JWT access token.
4. Use the token through the Swagger **Authorize** button or send it in the request header:

```text
Authorization: Bearer your_access_token
```

Protected endpoints automatically identify the current user from the token.

Users do not send their own `user_id` when creating or viewing financial data.

## API Endpoints

### Register

```http
POST /register
```

Example request:

```json
{
  "username": "erkan",
  "password": "secure-password"
}
```

Example response:

```json
{
  "user_id": 1,
  "username": "erkan"
}
```

### Login

```http
POST /login
```

The login endpoint uses OAuth2 form data.

Example response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

### Current User

```http
GET /me
```

Returns the authenticated user's public information.

### Create Transaction

```http
POST /transactions
```

Authentication is required.

Example income request:

```json
{
  "amount": 2500.00,
  "transaction_type": "income",
  "category": "Salary"
}
```

Example expense request:

```json
{
  "amount": 120.50,
  "transaction_type": "expense",
  "category": "Groceries"
}
```

The transaction is automatically assigned to the authenticated user.

### View Transactions

```http
GET /transactions
```

Returns only the authenticated user's transactions.

### View Balance

```http
GET /balance
```

The balance is calculated from all transactions:

```text
balance = total income - total expenses
```

The balance is not stored separately in the database.

## Validation and Error Handling

The API includes validation for:

* Username and password length
* Duplicate usernames
* Positive transaction amounts
* Supported transaction types
* Missing or invalid JWT tokens
* Expired JWT tokens

Common status codes:

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
422 Validation Error
```

## Security

* Passwords are never stored as plain text.
* Passwords are hashed with bcrypt.
* Protected endpoints require JWT authentication.
* Financial data is associated with the user identified by the token.
* Secret keys are loaded from environment variables.
* The `.env` file is excluded from version control.

## Current Scope

This repository contains the first version of the backend API.

The current scope includes:

* Authentication
* Income transactions
* Expense transactions
* Transaction history
* Balance calculation

Possible future improvements include:

* Automated tests
* Transaction update and deletion
* Category management
* Date filtering
* Pagination
* Monthly reports
* Docker support
* Database migrations with Alembic
* Frontend integration

## Author

Erkan Software Developer

GitHub: `ErkanSoftwareDeveloper`
