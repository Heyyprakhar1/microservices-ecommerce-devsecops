import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv
    ("DATABASE_URL", "mysql+pymysql://user:password@localhost:3306/productdb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-change-in-prod")
