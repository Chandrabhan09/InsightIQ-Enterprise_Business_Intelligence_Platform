import pandas as pd
from database.models import Manufacturer
from database.session import SessionLocal
from database.models import Car
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import func
import shutil
import os
import pandas as pd

class DatabaseService:

    @staticmethod
    def import_dataset(filepath):

        session = SessionLocal()

        try:

            if session.query(Car).count() > 0:

                return {
                    "message": "Database already contains data."
                }
            DatabaseService.create_default_manufacturer()
            manufacturer = session.query(
                Manufacturer
            ).filter(
                Manufacturer.name == "Ford"
            ).first()

            df = pd.read_csv(filepath)

            for _, row in df.iterrows():

                car = Car(

                    model=row["model"],

                    year=int(row["year"]),

                    price=int(row["price"]),

                    transmission=row["transmission"],

                    mileage=int(row["mileage"]),

                    fuel_type=row["fuelType"],

                    tax=int(row["tax"]),

                    mpg=float(row["mpg"]),

                    engine_size=float(row["engineSize"])
                )

                session.add(car)

            session.commit()

            return {

                "message": "Dataset imported successfully.",

                "rows_imported": len(df)

            }

        finally:

            session.close()
    
    @staticmethod
    def create_car(car_data):

        session = SessionLocal()

        try:

            car = Car(**car_data)

            session.add(car)

            session.commit()

            session.refresh(car)

            return {
                "message": "Car created successfully.",
                "id": car.id
            }

        finally:

            session.close()
    
    @staticmethod
    def get_all_cars():

        session = SessionLocal()

        try:

            cars = session.query(Car).all()

            return [
                {
                    "id": car.id,
                    "model": car.model,
                    "year": car.year,
                    "price": car.price,
                    "transmission": car.transmission,
                    "mileage": car.mileage,
                    "fuel_type": car.fuel_type,
                    "tax": car.tax,
                    "mpg": car.mpg,
                    "engine_size": car.engine_size,
                    "manufacturer_id": car.manufacturer_id
                }
                for car in cars
            ]

        finally:

            session.close()
    
    @staticmethod
    def get_car(car_id):

        session = SessionLocal()

        try:

            car = session.query(Car).filter(
                Car.id == car_id
            ).first()

            if not car:

                return None

            return {
                "id": car.id,
                "model": car.model,
                "year": car.year,
                "price": car.price,
                "transmission": car.transmission,
                "mileage": car.mileage,
                "fuel_type": car.fuel_type,
                "tax": car.tax,
                "mpg": car.mpg,
                "engine_size": car.engine_size
            }

        finally:

            session.close()
    
    @staticmethod
    def delete_car(car_id):

        session = SessionLocal()

        try:

            car = session.query(Car).filter(
                Car.id == car_id
            ).first()

            if not car:

                return None

            session.delete(car)

            session.commit()

            return {
                "message": "Car deleted successfully."
            }

        finally:

            session.close()
    
    @staticmethod
    def filter_cars(
        model=None,
        fuel_type=None,
        min_price=None,
        max_price=None,
        sort_by="price",
        order="asc"
    ):

        session = SessionLocal()

        try:

            query = session.query(Car)

            if model:

                query = query.filter(
                    Car.model.ilike(f"%{model}%")
                )

            if fuel_type:

                query = query.filter(
                    Car.fuel_type == fuel_type
                )

            if min_price is not None:

                query = query.filter(
                    Car.price >= min_price
                )

            if max_price is not None:

                query = query.filter(
                    Car.price <= max_price
                )

            sort_column = getattr(Car, sort_by, Car.price)

            if order.lower() == "desc":

                query = query.order_by(
                    sort_column.desc()
                )

            else:

                query = query.order_by(
                    sort_column.asc()
                )

            cars = query.all()

            return [

                {
                    "id": car.id,
                    "model": car.model,
                    "year": car.year,
                    "price": car.price,
                    "transmission": car.transmission,
                    "mileage": car.mileage,
                    "fuel_type": car.fuel_type,
                    "tax": car.tax,
                    "mpg": car.mpg,
                    "engine_size": car.engine_size
                }

                for car in cars

            ]

        finally:

            session.close()
    
    @staticmethod
    def aggregate_statistics():

        session = SessionLocal()

        try:

            return {

                "total_cars":
                    session.query(Car).count(),

                "average_price":
                    session.query(
                        func.avg(Car.price)
                    ).scalar(),

                "minimum_price":
                    session.query(
                        func.min(Car.price)
                    ).scalar(),

                "maximum_price":
                    session.query(
                        func.max(Car.price)
                    ).scalar(),

                "average_mileage":
                    session.query(
                        func.avg(Car.mileage)
                    ).scalar()

            }

        finally:

            session.close()
    
    @staticmethod
    def create_default_manufacturer():

        session = SessionLocal()

        try:

            manufacturer = session.query(
                Manufacturer
            ).filter(
                Manufacturer.name == "Ford"
            ).first()

            if manufacturer:

                return

            manufacturer = Manufacturer(
                name="Ford"
            )

            session.add(manufacturer)

            session.commit()

        finally:

            session.close()

    @staticmethod
    def cars_with_manufacturer():

        session = SessionLocal()

        try:

            results = (

                session.query(
                    Car,
                    Manufacturer
                )

                .join(
                    Manufacturer,
                    Car.manufacturer_id
                    ==
                    Manufacturer.id
                )

                .all()

            )

            return [

                {

                    "car_id": car.id,

                    "manufacturer": manufacturer.name,

                    "model": car.model,

                    "year": car.year,

                    "price": car.price,

                    "fuel_type": car.fuel_type

                }

                for car, manufacturer in results

            ]

        finally:

            session.close()

    @staticmethod
    def cars_above_average_price():

        session = SessionLocal()

        try:

            avg_price_subquery = (
                session.query(
                    func.avg(Car.price)
                ).scalar_subquery()
            )

            cars = (

                session.query(Car)

                .filter(
                    Car.price > avg_price_subquery
                )

                .all()

            )

            return [

                {

                    "id": car.id,

                    "model": car.model,

                    "price": car.price,

                    "year": car.year,

                    "fuel_type": car.fuel_type

                }

                for car in cars

            ]

        finally:

            session.close()

    @staticmethod
    def manufacturer_summary():

        session = SessionLocal()

        try:

            manufacturer_cte = (

                select(

                    Manufacturer.name.label("manufacturer"),

                    func.count(Car.id).label("total_cars"),

                    func.avg(Car.price).label("average_price")

                )

                .join(
                    Car,
                    Manufacturer.id == Car.manufacturer_id
                )

                .group_by(
                    Manufacturer.name
                )

                .cte("manufacturer_summary")

            )

            result = session.execute(

                select(manufacturer_cte)

            ).all()

            return [

                {

                    "manufacturer": row.manufacturer,

                    "total_cars": row.total_cars,

                    "average_price": round(
                        row.average_price,
                        2
                    )

                }

                for row in result

            ]

        finally:
            session.close()

    @staticmethod
    def get_car_summary():
        session = SessionLocal()
        try:
            result = session.execute(
                text("SELECT * FROM car_summary")
            )
            return [
                dict(row._mapping)
                for row in result
            ]
        finally:
            session.close()
        

    @staticmethod
    def bulk_price_update(increase_percent):

        session = SessionLocal()

        try:

            cars = session.query(Car).all()

            for car in cars:

                car.price = int(
                    car.price * (1 + increase_percent / 100)
                )

            session.commit()

            return {

                "message": "Prices updated successfully.",

                "updated_rows": len(cars)

            }

        except Exception as e:

            session.rollback()

            return {

                "message": "Transaction rolled back.",

                "error": str(e)

            }

        finally:

            session.close()

    @staticmethod
    def get_all_cars(db: Session):

        cars = db.query(Car).all()

        return [

        {

            "id": car.id,

            "model": car.model,

            "year": car.year,

            "price": car.price,

            "transmission": car.transmission,

            "mileage": car.mileage,

            "fuel_type": car.fuel_type,

            "tax": car.tax,

            "mpg": car.mpg,

            "engine_size": car.engine_size

        }

        for car in cars

    ]
        

    @staticmethod
    def dashboard_summary(db: Session):

        return {

        "total_cars":
            db.query(Car).count(),

        "average_price":
            round(
                db.query(
                    func.avg(Car.price)
                ).scalar(),
                2
            ),

        "minimum_price":
            db.query(
                func.min(Car.price)
            ).scalar(),

        "maximum_price":
            db.query(
                func.max(Car.price)
            ).scalar(),

        "average_mileage":
            round(
                db.query(
                    func.avg(Car.mileage)
                ).scalar(),
                2
            )

    }

    @staticmethod
    def average_price_by_model(db: Session):

     results = (

        db.query(

            Car.model,

            func.avg(Car.price)

        )

        .group_by(Car.model)

        .order_by(Car.model)

        .all()

    )

     return [

        {

            "model": model,

            "average_price": round(price,2)

        }

        for model, price in results

    ]
   

    @staticmethod
    def dashboard_summary(db: Session):

     return {

        "total_cars":
            db.query(Car).count(),

        "average_price":
            round(
                db.query(
                    func.avg(Car.price)
                ).scalar(),
                2
            ),

        "minimum_price":
            db.query(
                func.min(Car.price)
            ).scalar(),

        "maximum_price":
            db.query(
                func.max(Car.price)
            ).scalar(),

        "average_mileage":
            round(
                db.query(
                    func.avg(Car.mileage)
                ).scalar(),
                2
            )

    }

    @staticmethod
    def average_price_by_model(db: Session):

     results = (

        db.query(

            Car.model,

            func.avg(Car.price)

        )

        .group_by(Car.model)

        .order_by(Car.model)

        .all()

    )

     return [

        {

            "model": model,

            "average_price": round(price,2)

        }

        for model, price in results

    ]

    @staticmethod
    def fuel_distribution(db: Session):

     results = (

        db.query(

            Car.fuel_type,

            func.count(Car.id)

        )

        .group_by(Car.fuel_type)

        .all()

    )

     return [

        {

            "fuel_type": fuel,

            "count": total

        }

        for fuel, total in results

    ]

    @staticmethod
    def cars_by_year(db: Session):

     results = (

        db.query(

            Car.year,

            func.count(Car.id)

        )

        .group_by(Car.year)

        .order_by(Car.year)

        .all()

    )

     return [

        {

            "year": year,

            "count": total

        }

        for year, total in results

    ]

    @staticmethod
    def backup_database():

       source = "database/insightiq.db"

       destination = "backups/insightiq_backup.db"

       os.makedirs("backups", exist_ok=True)

       shutil.copy2(source, destination)

       return {

        "message": "Database backup created successfully.",

        "backup_location": destination

    }

    @staticmethod
    def restore_database():
        backup = "backups/insightiq_backup.db"
        database = "database/insightiq.db"
        if not os.path.exists(backup):
           return {
            "message": "Backup file not found."
           }

        shutil.copy2(backup, database)
        return {
        "message": "Database restored successfully."
        }
    
    @staticmethod
    def export_cars(db: Session):

       cars = db.query(Car).all()

       data = [

        {

            "id": car.id,

            "model": car.model,

            "year": car.year,

            "price": car.price,

            "transmission": car.transmission,

            "mileage": car.mileage,

            "fuel_type": car.fuel_type,

            "tax": car.tax,

            "mpg": car.mpg,

            "engine_size": car.engine_size

        }

          for car in cars

    ]

       os.makedirs(

        "exports",

        exist_ok=True

    )

       df = pd.DataFrame(data)

       filepath = "exports/cars_export.csv"

       df.to_csv(

        filepath,

        index=False

    )

       return {

        "message": "CSV exported successfully.",

        "file": filepath

    }

@staticmethod
def export_dashboard_report(db: Session):

    report = DatabaseService.dashboard_summary(db)

    os.makedirs(

        "exports",

        exist_ok=True

    )

    df = pd.DataFrame(

        [report]

    )

    filepath = "exports/dashboard_report.csv"

    df.to_csv(

        filepath,

        index=False

    )

    return {

        "message": "Dashboard exported successfully.",

        "file": filepath

    }