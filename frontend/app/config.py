import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    API_URL = os.getenv('API_URL', 'http://backend:8000')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@artutos.eu.org')
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'admin.artutos.us.kg').split(',')
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = '/tmp/flask_session'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds
    
    # Ensure the session directory exists
    os.makedirs(SESSION_FILE_DIR, exist_ok=True)