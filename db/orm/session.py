from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import db.config as config

engine = create_engine(config.DB_URL)
SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()
