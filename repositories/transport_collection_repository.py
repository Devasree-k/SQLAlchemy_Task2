
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from models.driver_model import Driver
from models.transport_collection_model import TransportCollection


def get_driver(db: Session, driver_id: int):
    return db.get(Driver, driver_id)


def create(db: Session, collection: TransportCollection):
    db.add(collection)
    db.flush()
    return collection


def get_by_id(db: Session, collection_id: int):
    statement = (
        select(TransportCollection)
        .options(joinedload(TransportCollection.driver))
        .where(TransportCollection.id == collection_id)
    )
    return db.scalars(statement).unique().first()


def get_all(db: Session):
    statement = (
        select(TransportCollection)
        .options(joinedload(TransportCollection.driver))
        .order_by(TransportCollection.id)
    )
    return list(db.scalars(statement).unique().all())


def delete(db: Session, collection: TransportCollection):
    db.delete(collection)
    db.flush()
