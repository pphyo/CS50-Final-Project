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

def get_db():
    """Create database connection"""
    db = sqlite3.connect("balance.db")
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database"""
    with get_db() as db:
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())