import mysql.connector
from config import MYSQL_CONFIG

conn = mysql.connector.connect(**MYSQL_CONFIG)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")

conn.commit()
cursor.close()
conn.close()
