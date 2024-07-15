from dotenv import load_dotenv
import os

load_dotenv()

class config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATION = ""
    UPLOAD_FOLDER = 'uploads'

class devConfig:
    DEBUG = True
    SQL_DB_URI = ""
    UPLOAD_FOLDER = 'uploads'