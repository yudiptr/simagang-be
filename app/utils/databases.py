from contextlib import contextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.config import Config


engine = create_engine(Config.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        session.begin()
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        