from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///database/insightiq.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)