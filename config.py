import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Use SQLite with absolute path for Render's persistent disk
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'instance', 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    # App Settings
    QUIZ_QUESTIONS_COUNT = int(os.environ.get('QUIZ_QUESTIONS_COUNT', '10'))