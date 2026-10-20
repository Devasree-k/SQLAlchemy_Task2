# from fastapi import HTTPException
# from sqlalchemy import select,func 

# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import Session, joinedload,selectinload
# from models.driver_model import Driver

# from decimal import Decimal
# from datetime import date
# from models.transport_collection_model import TransportCollection


# def create_driver(db: Session, data):
#     driver = Driver(**data.model_dump())
#     db.add(driver)
#     try:
#         db.commit()
#         db.refresh(driver)
#         return driver
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=409, detail="Phone number already exists")

# def get_drivers(db: Session):
#     return list(db.scalars(select(Driver).order_by(Driver.id)).all())

# def get_driver(db: Session, driver_id: int):
#     driver = db.get(Driver, driver_id)
#     if driver is None:
#         raise HTTPException(status_code=404, detail="Driver not found")
#     return driver


# def get_driver_with_collection(db:Session, driver_id= int):
#     statement = (select(Driver)
#                  .options(selectinload(Driver.collections))
#                  .where(Driver.id==driver_id))

#     driver = db.scalars(statement).unique().first()
#     if driver is None:
#         raise HTTPException(status_code=404, detail="Driver id not found")
#     return driver


# # def get_driver_report(db:Session, 
# #                       start_date: date | None = None,
# #                       end_date : date | None = None):

# #     statement = (
# #         select(
# #             Driver.id.label("driver_id"),
# #             Driver.name.label("driver_name"),
# #             func.count(TransportCollection.id).label("total_records"),
# #             func.sum(TransportCollection.total_trips).label("total_trips"),
# #             func.sum(TransportCollection.total_collection).label("total_collection"),
# #             func.sum(TransportCollection.total_expense).label("total_expense"),
# #             func.sum(TransportCollection.net_collection).label("net_collection"),
# #             func.max(TransportCollection.total_collection).label("highest_collection"),
            
# #         ).join(TransportCollection, Driver.id==TransportCollection.driver_id)
# #     )

# #     if start_date is not None:
# #         statement = statement.where(
# #             TransportCollection.collection_date >= start_date
# #         )

# #     if end_date is not None:
# #         statement = statement.where(
# #             TransportCollection.collection_date <= end_date
# #         )

# #     statement = statement.group_by(
# #         Driver.id,
# #         Driver.name,
# #     ).order_by(Driver.id)

# #     return db.execute(statement).mappings().all()



# def get_driver_report(
#     db: Session,
#     start_date: date | None = None,
#     end_date: date | None = None,
#     minimum_net: Decimal | None = None,
# ):
#     statement = (
#         select(
#             Driver.id.label("driver_id"),
#             Driver.name.label("driver_name"),
#             func.count(
#                 TransportCollection.id
#             ).label("total_records"),
#             func.sum(
#                 TransportCollection.total_trips
#             ).label("total_trips"),
#             func.sum(
#                 TransportCollection.total_collection
#             ).label("total_collection"),
#             func.sum(
#                 TransportCollection.total_expense
#             ).label("total_expense"),
#             func.sum(
#                 TransportCollection.net_collection
#             ).label("net_collection"),
#             func.avg(
#                 TransportCollection.total_collection
#             ).label("average_collection"),
#             func.max(
#                 TransportCollection.total_collection
#             ).label("highest_collection"),
#         )
#         .join(
#             TransportCollection,
#             Driver.id == TransportCollection.driver_id,
#         )
#     )

#     # WHERE: filter individual collection records.
#     if start_date is not None:
#         statement = statement.where(
#             TransportCollection.collection_date >= start_date
#         )

#     if end_date is not None:
#         statement = statement.where(
#             TransportCollection.collection_date <= end_date
#         )

#     # GROUP BY: create one result row per driver.
#     statement = statement.group_by(
#         Driver.id,
#         Driver.name,
#     )

#     # HAVING: filter drivers after calculating their totals.
#     if minimum_net is not None:
#         statement = statement.having(
#             func.sum(
#                 TransportCollection.net_collection
#             ) >= minimum_net
#         )

#     # ORDER BY: highest net collection first.
#     statement = statement.order_by(
#         func.sum(
#             TransportCollection.net_collection
#         ).desc()
#     )

#     return db.execute(statement).mappings().all()


from datetime import date

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.driver_model import Driver
from models.transport_collection_model import TransportCollection
from repositories import driver_repository


def create_driver(db: Session, data):
    driver = Driver(**data.model_dump())

    try:
        driver_repository.create(db, driver)
        db.commit()
        db.refresh(driver)
        return driver
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Phone number already exists",
        ) from exc


def get_drivers(db: Session):
    return driver_repository.get_all(db)


def get_driver(db: Session, driver_id: int):
    driver = driver_repository.get_by_id(db, driver_id)

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found",
        )

    return driver


def get_driver_with_collection(db: Session, driver_id: int):
    driver = driver_repository.get_with_collections(db, driver_id)

    if driver is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found",
        )

    return driver


def get_driver_report(
    db: Session,
    start_date: date | None = None,
    end_date: date | None = None,
):
    statement = (
        select(
            Driver.id.label("driver_id"),
            Driver.name.label("driver_name"),
            func.count(TransportCollection.id).label("total_records"),
            func.coalesce(
                func.sum(TransportCollection.total_trips), 0
            ).label("total_trips"),
            func.coalesce(
                func.sum(TransportCollection.total_collection), 0
            ).label("total_collection"),
            func.coalesce(
                func.sum(TransportCollection.total_expense), 0
            ).label("total_expense"),
            func.coalesce(
                func.sum(TransportCollection.net_collection), 0
            ).label("net_collection"),
            func.max(
                TransportCollection.total_collection
            ).label("highest_collection"),
        )
        .outerjoin(
            TransportCollection,
            Driver.id == TransportCollection.driver_id,
        )
        .group_by(Driver.id, Driver.name)
        .order_by(Driver.id)
    )

    if start_date is not None:
        statement = statement.where(
            (TransportCollection.collection_date >= start_date)
            | (TransportCollection.id.is_(None))
        )
 
    if end_date is not None:
        statement = statement.where(
            (TransportCollection.collection_date <= end_date)
            | (TransportCollection.id.is_(None))
        )

    return db.execute(statement).mappings().all()
