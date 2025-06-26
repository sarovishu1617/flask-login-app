from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session

# Initialize DB
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    phone = request.form['number']

    # Save to DB
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (email, phone) VALUES (?, ?)", (email, phone))
    conn.commit()
    conn.close()

    # Generate OTP and store in session
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    session['email'] = email
    session['phone'] = phone

    print("OTP:", otp)  # For now print in terminal

    return render_template('verify.html', otp=otp)  # Show on screen for testing

@app.route('/verify', methods=['POST'])
def verify():
    user_otp = request.form['otp']
    actual_otp = session.get('otp')

    if user_otp == actual_otp:
        return f"<h2>Login Successful ✅</h2><p>Welcome, {session.get('email')}</p>"
    else:
        return "<h2>❌ Invalid OTP</h2><p><a href='/'>Try again</a></p>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
