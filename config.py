import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Use PostgreSQL on Render, SQLite locally
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    
    # Fix for Render's postgres:// vs postgresql:// URL format
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    # App Settings
    QUIZ_QUESTIONS_COUNT = int(os.environ.get('QUIZ_QUESTIONS_COUNT', '10'))