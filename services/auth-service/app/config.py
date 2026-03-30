import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/authdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-change-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES = 3600 # 1 hour
