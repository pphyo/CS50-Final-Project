# Balance Management System

#### Video Demo: <https://youtu.be/AWgyDxRO8Zc>

#### Description

The Balance System is a Python Flask web application designed to empower users with a user-friendly and secure platform for managing their finances. This project prioritizes both functionality and security, providing key features like user authentication, account management, transaction tracking, and a focus on data protection.

Built with simplicity in mind, the Balance System caters to individuals seeking a straightforward way to monitor their financial activities. It utilizes an SQLite database for efficient data storage and retrieval.
System Functionality

The Balance System offers a comprehensive set of features to streamline personal finance management:

Secure User Authentication:
    Users register and create unique accounts protected by strong password hashing with the bcrypt algorithm and a random salt. This ensures one-way encryption, making it impossible to decrypt passwords for unauthorized access.
    The login process verifies user credentials before granting access to sensitive account information.

Account Management:
    Users can view their current account balance in real-time, providing an instant financial snapshot.
    Deposit and withdraw functionalities allow users to update their account balance by adding or removing funds. The system enforces sufficient balance checks to prevent negative balances.
    A detailed transaction history tracks all financial activities, including timestamps, transaction types (deposit/withdrawal), and specific amounts. This comprehensive record enables users to monitor spending patterns and analyze their financial trends.

Security Features:
    The Balance System implements robust security measures to safeguard user data and prevent unauthorized access:
        User input is validated to prevent SQL injection attacks and cross-site scripting (XSS) vulnerabilities. This protects the application from malicious code injection attempts.
        Session-based authentication is employed, assigning unique session identifiers to users upon successful login. This prevents unauthorized access to user accounts even if login credentials are compromised.
        Transaction verification ensures data integrity by guaranteeing the accuracy and authenticity of recorded financial transactions.

Technical Details

    Development Environment:
        Programming Language: Python 3 (compatible with most recent versions)
        Web Framework: Flask (lightweight and flexible web application framework)
    Data Storage:
        Database: SQLite (lightweight embedded relational database management system)
    Security Measures:
        Password Hashing: bcrypt algorithm with random salt
        Input Validation: Sanitization checks to prevent malicious code injection
        Session Management: Session-based user authentication
        Transaction Verification: Ensures data integrity of recorded transactions

## How to run

`pip install -r requirements.txt`

And open the python shell and enter below command to initialize database

`from helpers import init_db`

`init_db()`

And then

`flask run`
