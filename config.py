MONGO_URI = "mongodb+srv://sugash:Sugash28s@cluster0.i5u0el5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# config.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

MYSQL_CONFIG = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'port': int(os.getenv('MYSQL_PORT')),
    'database': os.getenv('MYSQL_DB')
}
