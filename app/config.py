from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

class Config:
    DB_PORT = os.getenv("DB_PORT")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_HASH_METHOD = os.getenv("JWT_HASH_METHOD")
    