from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from config import MYSQL_CONFIG

app = Flask(__name__)
CORS(app)


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

if __name__ == '__main__':
    app.run(debug=True)
