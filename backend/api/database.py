import os
from fastapi import Body
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi import Body
from fastapi import Depends
from sqlalchemy.orm import Session
from database.session import get_db
from services.database_service import DatabaseService

router = APIRouter(
    prefix="/api/database",
    tags=["Database"]
)

@router.post("/cars")
def create_car(car: dict = Body(...)):
    return DatabaseService.create_car(car)

@router.get("/cars/{car_id}")
def get_car(car_id: int):

    car = DatabaseService.get_car(car_id)

    if car is None:

        raise HTTPException(
            status_code=404,
            detail="Car not found."
        )

    return car

@router.put("/cars/{car_id}")
def update_car(
    car_id: int,
    updated_data: dict = Body(...)
):

    result = DatabaseService.update_car(
        car_id,
        updated_data
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Car not found."
        )

    return result

@router.delete("/cars/{car_id}")
def delete_car(car_id: int):

    result = DatabaseService.delete_car(car_id)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Car not found."
        )

    return result

@router.get("/import")
def import_dataset(
    filepath: str = Query(...)
):

    if not os.path.exists(filepath):

        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    return DatabaseService.import_dataset(filepath)

@router.get("/cars/filter")
def filter_cars(

    model: str = Query(None),

    fuel_type: str = Query(None),

    min_price: int = Query(None),

    max_price: int = Query(None),

    sort_by: str = Query("price"),

    order: str = Query("asc")

):

    return DatabaseService.filter_cars(

        model,

        fuel_type,

        min_price,

        max_price,

        sort_by,

        order

    )

@router.get("/cars/statistics")
def statistics():

    return DatabaseService.aggregate_statistics()

@router.get("/cars-with-manufacturer")
def cars_with_manufacturer():

    return DatabaseService.cars_with_manufacturer()

@router.get("/cars/above-average-price")
def cars_above_average_price():

    return DatabaseService.cars_above_average_price()

@router.get("/manufacturer-summary")
def manufacturer_summary():

    return DatabaseService.manufacturer_summary()

@router.get("/car-summary")
def car_summary():

    return DatabaseService.get_car_summary()

@router.put("/bulk-price-update")
def bulk_price_update(
    increase_percent: float = Body(...)
):

    return DatabaseService.bulk_price_update(
        increase_percent
    )

@router.get("/analytics/dashboard")
def dashboard(

    db: Session = Depends(get_db)

):

    return DatabaseService.dashboard_summary(db)

@router.get("/analytics/average-price")
def average_price(

    db: Session = Depends(get_db)

):

    return DatabaseService.average_price_by_model(db)

@router.get("/analytics/fuel-distribution")
def fuel_distribution(

    db: Session = Depends(get_db)

):

    return DatabaseService.fuel_distribution(db)

@router.get("/analytics/year-distribution")
def year_distribution(

    db: Session = Depends(get_db)

):

    return DatabaseService.cars_by_year(db)

@router.post("/backup")
def backup_database():

    return DatabaseService.backup_database()

@router.post("/restore")
def restore_database():

    return DatabaseService.restore_database()

@router.get("/export/cars")
def export_cars(

    db: Session = Depends(get_db)

):

    return DatabaseService.export_cars(db)
@router.get("/export/dashboard")
def export_dashboard(

    db: Session = Depends(get_db)

):

    return DatabaseService.export_dashboard_report(db)