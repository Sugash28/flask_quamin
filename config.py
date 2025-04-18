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

MAIL_CONFIG = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': 'quamin_agricare',
    'MAIL_PASSWORD': "lnzo ipkz ewty lyie",
    'MAIL_DEFAULT_SENDER': "sugashsugu@gmail.com"
}
