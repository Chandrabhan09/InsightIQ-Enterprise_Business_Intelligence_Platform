from sqlalchemy import text

from database.connection import engine


def create_views():

    with engine.begin() as connection:

        connection.execute(text("""

        CREATE VIEW IF NOT EXISTS car_summary AS

        SELECT

            c.id,

            c.model,

            c.year,

            c.price,

            c.fuel_type,

            m.name AS manufacturer

        FROM cars c

        INNER JOIN manufacturers m

        ON c.manufacturer_id = m.id

        """))