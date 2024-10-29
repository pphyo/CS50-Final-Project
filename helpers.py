import sqlite3
from flask import redirect, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect("balance.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database"""
    with get_db_connection() as db:
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())

def get_user_balance(user_id):
    conn = get_db_connection()
    balance = conn.execute('SELECT amount FROM balances WHERE user_id = ?', 
                         (user_id,)).fetchone()
    conn.close()
    return float(balance['amount']) if balance else 0.0

def update_balance(user_id, amount, type):
    conn = get_db_connection()
    try:
        current_balance = get_user_balance(user_id)
        
        if type == 'withdraw' and current_balance < amount:
            return False, "Insufficient balance."
        
        new_balance = current_balance + amount if type == 'deposit' else current_balance - amount
        
        # Begin Transaction
        conn.execute('BEGIN TRANSACTION')
        
        # update balances table
        conn.execute('''
            INSERT INTO balances (user_id, amount, last_updated)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                amount = ?,
                last_updated = CURRENT_TIMESTAMP
        ''', (user_id, new_balance, new_balance))
        
        # insert transactions table
        conn.execute('''
            INSERT INTO transactions (user_id, type, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (user_id, type, amount, f"{type.title()} transaction"))
        
        conn.commit()
        return True, "Success"
        
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()

def get_transaction_history(user_id):
    conn = get_db_connection()
    transactions = conn.execute('''
        SELECT id, type, amount, description, created_at 
        FROM transactions 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return transactions