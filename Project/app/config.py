import os

# This configures the database connection
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nope'
    
    # PostgreSQL configuration
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    PUBLIC_IP = os.environ.get('PUBLIC_IP')
    DB_NAME = os.environ.get('DB_NAME')
    
    # fall back to SQLite for local development if no DATABASE_URL is set
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{PUBLIC_IP}:5432/{DB_NAME}" \
        if DB_USER and DB_PASSWORD and PUBLIC_IP and DB_NAME else \
        'sqlite:///app.db'
    print(f"$$$$$$$$$$$$$$$$$:\n {SQLALCHEMY_DATABASE_URI}\n$$$$$$$$$$$$$$$$$$$$$")
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
