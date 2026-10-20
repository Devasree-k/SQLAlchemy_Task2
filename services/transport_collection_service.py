# from decimal import Decimal
# from fastapi import HTTPException
# from sqlalchemy import select
# from sqlalchemy.orm import Session, joinedload
# from models.driver_model import Driver
# from models.transport_collection_model import TransportCollection

# def calculate_totals(data: dict) -> dict:
#     total_trips = data["morning_trips"] + data["evening_trips"]
#     total_collection = data["morning_collection"] + data["evening_collection"]
#     total_expense = data["fuel_expense"] + data["other_expense"]
#     return {
#         "total_trips": total_trips,
#         "total_collection": total_collection,
#         "total_expense": total_expense,
#         "net_collection": total_collection - total_expense,
#     }

# def collection_query():
#     # Load the related Driver in the same SQL query.
#     return select(TransportCollection).options(
#         joinedload(TransportCollection.driver)
#     )

# def get_collection_or_404(db: Session, collection_id: int):
#     statement = collection_query().where(TransportCollection.id == collection_id)
#     collection = db.scalars(statement).unique().first()
#     if collection is None:
#         raise HTTPException(status_code=404, detail="Collection not found")
#     return collection

# def create_collection(db: Session, data):
#     values = data.model_dump()
#     if db.get(Driver, values["driver_id"]) is None:
#         raise HTTPException(status_code=404, detail="Driver not found")
#     values.update(calculate_totals(values))
#     collection = TransportCollection(**values)
#     db.add(collection)
#     db.commit()
#     return get_collection_or_404(db, collection.id)

# def get_collections(db: Session):
#     statement = collection_query().order_by(TransportCollection.id)
#     return list(db.scalars(statement).unique().all())

# def get_collection(db: Session, collection_id: int):
#     return get_collection_or_404(db, collection_id)

# def update_collection(db: Session, collection_id: int, changes: dict):
#     collection = get_collection_or_404(db, collection_id)
#     values = {
#         "driver_id": collection.driver_id,
#         "vehicle_number": collection.vehicle_number,
#         "collection_date": collection.collection_date,
#         "morning_trips": collection.morning_trips,
#         "evening_trips": collection.evening_trips,
#         "morning_collection": collection.morning_collection,
#         "evening_collection": collection.evening_collection,
#         "fuel_expense": collection.fuel_expense,
#         "other_expense": collection.other_expense,
#     }
#     values.update(changes)
#     if db.get(Driver, values["driver_id"]) is None:
#         raise HTTPException(status_code=404, detail="Driver not found")
#     for field, value in changes.items():
#         setattr(collection, field, value)
#     for field, value in calculate_totals(values).items():
#         setattr(collection, field, value)
#     db.commit()
#     return get_collection_or_404(db, collection_id)

# def delete_collection(db: Session, collection_id: int):
#     collection = get_collection_or_404(db, collection_id)
#     db.delete(collection)
#     db.commit()
#     return {"message": "Collection deleted"}

from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.transport_collection_model import TransportCollection
from repositories import transport_collection_repository as repository


def calculate_totals(data: dict) -> dict:
    total_trips = data["morning_trips"] + data["evening_trips"]
    total_collection = (
        data["morning_collection"] + data["evening_collection"]
    )
    total_expense = data["fuel_expense"] + data["other_expense"]

    return {
        "total_trips": total_trips,
        "total_collection": total_collection,
        "total_expense": total_expense,
        "net_collection": total_collection - total_expense,
    }


def get_collection_or_404(db: Session, collection_id: int):
    collection = repository.get_by_id(db, collection_id)

    if collection is None:
        raise HTTPException(
            status_code=404,
            detail="Collection not found",
        )

    return collection


def create_collection(db: Session, data):
    values = data.model_dump()

    if repository.get_driver(db, values["driver_id"]) is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    values.update(calculate_totals(values))
    collection = TransportCollection(**values)

    try:
        repository.create(db, collection)
        db.commit()
        return get_collection_or_404(db, collection.id)
    except Exception:
        db.rollback()
        raise


def get_collections(db: Session):
    return repository.get_all(db)


def get_collection(db: Session, collection_id: int):
    return get_collection_or_404(db, collection_id)


def update_collection(db: Session, collection_id: int, changes: dict):
    collection = get_collection_or_404(db, collection_id)

    values = {
        "driver_id": collection.driver_id,
        "vehicle_number": collection.vehicle_number,
        "collection_date": collection.collection_date,
        "morning_trips": collection.morning_trips,
        "evening_trips": collection.evening_trips,
        "morning_collection": collection.morning_collection,
        "evening_collection": collection.evening_collection,
        "fuel_expense": collection.fuel_expense,
        "other_expense": collection.other_expense,
    }

    values.update(changes)

    if repository.get_driver(db, values["driver_id"]) is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    calculated = calculate_totals(values)

    try:
        for field, value in changes.items():
            setattr(collection, field, value)

        for field, value in calculated.items():
            setattr(collection, field, value)

        db.commit()
        return get_collection_or_404(db, collection_id)
    except Exception:
        db.rollback()
        raise


def delete_collection(db: Session, collection_id: int):
    collection = get_collection_or_404(db, collection_id)

    try:
        repository.delete(db, collection)
        db.commit()
        return {"message": "Collection deleted"}
    except Exception:
        db.rollback()
        raise
