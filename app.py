from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
import random
import mysql.connector
from config import MYSQL_CONFIG, MAIL_CONFIG
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Configuring the mail server
app.config.update(MAIL_CONFIG)
mail = Mail(app)

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({'status': 'fail', 'message': 'Email already registered'}), 409

    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({'status': 'success', 'message': 'Login successful'}), 200
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401

def generate_otp():
    """Generates a 6-digit OTP."""
    return random.randint(100000, 999999)

def send_otp_email(email, otp):
    """Sends OTP to the user's email."""
    msg = Message('Your OTP Code', recipients=[email])
    msg.body = f'Your OTP code is {otp}. It will expire in 5 minutes.'
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/send-otp', methods=['POST'])  # Hyphen matches Flutter
def send_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'status': 'fail', 'message': 'Email is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return jsonify({'status': 'fail', 'message': 'Email not registered'}), 404

    otp = generate_otp()
    otp_expiry = datetime.utcnow() + timedelta(minutes=5)

    cursor.execute("INSERT INTO otp_requests (email, otp, otp_expiry) VALUES (%s, %s, %s)", 
                   (email, otp, otp_expiry))
    conn.commit()

    cursor.close()
    conn.close()

    if send_otp_email(email, otp):
        return jsonify({'status': 'success', 'message': 'OTP sent to email'}), 200
    else:
        return jsonify({'status': 'fail', 'message': 'Failed to send OTP'}), 500

# In Flask's /validate-otp endpoint
@app.route('/validate-otp', methods=['POST'])
def validate_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if not email or not otp:
        return jsonify({'status': 'fail', 'message': 'Email and OTP required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch the most recent OTP for the email
    cursor.execute("""
        SELECT otp, otp_expiry 
        FROM otp_requests 
        WHERE email = %s 
        ORDER BY otp_expiry DESC 
        LIMIT 1
    """, (email,))
    otp_record = cursor.fetchone()

    if not otp_record:
        cursor.close()
        conn.close()
        return jsonify({'status': 'fail', 'message': 'OTP not found'}), 404

    otp_saved, otp_expiry = otp_record

    # Check OTP expiry
    if datetime.utcnow() > otp_expiry:
        cursor.close()
        conn.close()
        return jsonify({'status': 'fail', 'message': 'OTP expired'}), 400

    # Validate OTP (ensure both are strings)
    if str(otp_saved) == str(otp):
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'OTP validated'}), 200
    else:
        cursor.close()
        conn.close()
        return jsonify({'status': 'fail', 'message': 'Invalid OTP'}), 401

if __name__ == '__main__':
    app.run(debug=True)
