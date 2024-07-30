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
    

    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

    HASH_KEY = os.getenv("HASH_KEY")