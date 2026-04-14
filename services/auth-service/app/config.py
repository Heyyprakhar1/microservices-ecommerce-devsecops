import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/authdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-change-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES = 3600 # 1 hour

    # Google OAuth
    SECRET_KEY = os.getenv("SECRET_KEY", "flask-secret-change-in-prod")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:5001/api/auth/google/callback")
