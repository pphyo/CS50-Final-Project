# Balance System

## Project Information

- **Author**: Pyae Phyo
- **GitHub Username**: pphyo
- **edX Username**: pphyo206
- **Location**: Yangon, Myanmar
- **Date**: October 29, 2024

**Video Demo**: [URL HERE]  

**Description**:  
The Balance System is a comprehensive financial management application that allows users to manage their account balance through various operations. This project was developed to provide a simple yet effective way for users to handle their financial transactions.

## Features

### User Authentication

- Secure login system
- New user registration
- Password protection for all accounts

### Account Management

- Check current balance
- Deposit funds
- Withdraw funds
- View detailed transaction history

### Transaction History

- Complete log of all transactions
- Date and time stamps for each transaction
- Transaction type (deposit/withdrawal)
- Amount details

## Technical Details

- **Built using**: Python
- **Data persistence**: SQLite database
- **Security**: Secure password hashing
- **Error Handling**: Input validation and error handling
- **Interface**: User-friendly command-line interface

## How to Use

### Registration

1. Create a new account with a username and password.
2. The system automatically creates your account with a 0 balance.

### Login

- Access your account using registered credentials.
- View your current balance immediately upon login.

### Transactions

- **Deposit**: Add funds to your account.
- **Withdraw**: Remove funds from your account (subject to available balance).
- **History**: View all your past transactions.

## Security Features

- Encrypted password storage
- Session management
- Transaction verification
- Input sanitization

This Balance System provides a foundation for basic financial management while ensuring security and reliability. It's designed to be user-friendly while maintaining robust functionality.

## How to run

`pip install -r requirements.txt`

And open the python shell and enter below command to initialize database

`from helpers import init_db`

`init_db()`

And then

`flask run`
