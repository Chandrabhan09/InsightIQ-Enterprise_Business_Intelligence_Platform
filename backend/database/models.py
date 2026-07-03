from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, Float, String, ForeignKey


class Base(DeclarativeBase):
    pass


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    cars = relationship(
        "Car",
        back_populates="manufacturer"
    )


class Car(Base):
    __tablename__ = "cars"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    model = Column(
        String,
        nullable=False
    )

    year = Column(Integer)

    price = Column(Integer)

    transmission = Column(String)

    mileage = Column(Integer)

    fuel_type = Column(String)

    tax = Column(Integer)

    mpg = Column(Float)

    engine_size = Column(Float)

    manufacturer_id = Column(
        Integer,
        ForeignKey("manufacturers.id")
    )

    manufacturer = relationship(
        "Manufacturer",
        back_populates="cars"
    )

model = Column(
    String,
    nullable=False,
    index=True
)

price = Column(
    Integer,
    index=True
)

year = Column(
    Integer,
    index=True
)

fuel_type = Column(
    String,
    index=True
)