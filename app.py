"""
Student Portal - Sample Flask Application (VULNERABLE VERSION)
----------------------------------------------------------------
This is the intentionally insecure application selected for the
CodeAlpha Secure Coding Review task. It simulates a small student
login + feedback portal. It is used ONLY as a training/demo target
for a manual + automated security code review, NOT for production use.
"""

import sqlite3
import hashlib
import os
import pickle
from flask import Flask, request, render_template, render_template_string

app = Flask(__name__)

# --- VULNERABILITY 1: Hardcoded secret key committed to source code ---
app.secret_key = "s3cr3t_k3y_2024"

DB_PATH = "portal.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
    )
    conn.execute(
        "INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')"
    )
    conn.commit()
    conn.close()


@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # --- VULNERABILITY 2: SQL Injection via string concatenation ---
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    conn = get_db()
    cursor = conn.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return "Welcome " + username  # --- VULNERABILITY 3: Reflected XSS, no escaping ---
    return render_template("login.html", error="Invalid email address or password."), 401


@app.route("/hash_password", methods=["POST"])
def hash_password():
    password = request.form.get("password", "")
    # --- VULNERABILITY 4: Weak/broken hash algorithm (MD5) for passwords, no salt ---
    hashed = hashlib.md5(password.encode()).hexdigest()
    return {"hash": hashed}


@app.route("/ping", methods=["GET"])
def ping():
    host = request.args.get("host", "127.0.0.1")
    # --- VULNERABILITY 5: OS command injection via unsanitized user input ---
    result = os.system("ping -c 1 " + host)
    return f"Ping executed with exit code {result}"


@app.route("/profile", methods=["GET"])
def profile():
    name = request.args.get("name", "Guest")
    # --- VULNERABILITY 6: Server-Side Template Injection (SSTI) ---
    template = "<h1>Welcome, " + name + "!</h1>"
    return render_template_string(template)


@app.route("/load_session", methods=["POST"])
def load_session():
    # --- VULNERABILITY 7: Insecure deserialization with pickle on user input ---
    data = request.form.get("session_data", "")
    session_obj = pickle.loads(data.encode("latin1"))
    return {"loaded": str(session_obj)}


if __name__ == "__main__":
    init_db()
    # --- VULNERABILITY 8: Debug mode enabled in what could reach production ---
    app.run(debug=True, host="0.0.0.0")
