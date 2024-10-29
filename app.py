import sqlite3
from flask import Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, get_db_connection, update_balance, get_user_balance, get_transaction_history

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'your_secret_key_here'  # In production, use a proper secret key

@app.route("/")
@login_required
def index():
    """Show dashboard"""
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username", "error")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password", "error")
            return render_template("login.html")

        # Query database for username
        db = get_db_connection()
        user = db.execute("SELECT * FROM users WHERE username = ?",
                         [request.form.get("username")]).fetchone()

        # Ensure username exists and password is correct
        if user is None or not check_password_hash(user["password"], request.form.get("password")):
            flash("Invalid username and/or password", "error")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = user["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate input
        if not username:
            flash("Must provide username", "error")
            return render_template("register.html")
        elif not password:
            flash("Must provide password", "error")
            return render_template("register.html")
        elif not confirmation:
            flash("Must confirm password", "error")
            return render_template("register.html")
        elif password != confirmation:
            flash("Passwords must match", "error")
            return render_template("register.html")

        # Hash the password
        hash = generate_password_hash(password)

        try:
            db = get_db_connection()
            # Insert new user
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      [username, hash])
            # Create initial balance record
            user_id = db.execute("SELECT id FROM users WHERE username = ?",
                               [username]).fetchone()["id"]
            db.execute("INSERT INTO balances (user_id, amount) VALUES (?, 0)",
                      [user_id])
            db.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists", "error")
            return render_template("register.html")

        flash("Registered successfully!", "success")
        return redirect("/login")

    return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    flash("Successfully logged out", "success")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    print(user_id)
    balance = get_user_balance(user_id)
    transactions = get_transaction_history(user_id)
    return render_template("dashboard.html", balance=balance, transactions=transactions)

@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            if amount <= 0:
                flash("Incorrect amount", "error")
                return redirect(url_for("deposit"))
            
            success, message = update_balance(session["user_id"], amount, "deposit")
            flash(message, "success" if success else "error")
            return redirect(url_for("dashboard"))
            
        except ValueError:
            flash("Incorrect amount", "error")
            return redirect(url_for("deposit"))
            
    return render_template("deposit.html")

@app.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            if amount <= 0:
                flash("Incorrect amount", "error")
                return redirect(url_for("withdraw"))
            
            success, message = update_balance(session["user_id"], amount, "withdraw")
            flash(message, "success" if success else "error")
            return redirect(url_for("dashboard"))
            
        except ValueError:
            flash("Incorrect amount", "error")
            return redirect(url_for("withdraw"))
            
    return render_template("withdraw.html")

if __name__ == "__main__":
    app.run(debug=True)