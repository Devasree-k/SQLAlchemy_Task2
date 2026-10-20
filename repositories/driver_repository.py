
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models.driver_model import Driver


def create(db: Session, driver: Driver) -> Driver:
    db.add(driver)
    db.flush()
    return driver


def get_by_id(db: Session, driver_id: int):
    return db.get(Driver, driver_id)


def get_all(db: Session):
    statement = select(Driver).order_by(Driver.id)
    return list(db.scalars(statement).all())


def get_with_collections(db: Session, driver_id: int):
    statement = (
        select(Driver)
        .options(selectinload(Driver.collections))
        .where(Driver.id == driver_id)
    )
    return db.scalars(statement).first()


def phone_exists(
    db: Session,
    phone: str,
    exclude_driver_id: int | None = None,
) -> bool:
    statement = select(Driver.id).where(Driver.phone == phone)

    if exclude_driver_id is not None:
        statement = statement.where(Driver.id != exclude_driver_id)

    return db.scalar(statement) is not None
