from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from database.connection import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()