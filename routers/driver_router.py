# from fastapi import APIRouter, Depends, status, HTTPException, Query
# from sqlalchemy.orm import Session
# from dependencies.database import get_database

# from datetime import date
# from decimal import Decimal

# from schemas.driver_schema import DriverCreate, DriverResponse, DriverWithCollectionsResponse
# from services.driver_service import create_driver, get_driver, get_drivers,get_driver_with_collection, get_driver_report

# router = APIRouter(prefix="/api/drivers", 
#                    tags=["Drivers"]
#                    )



# @router.get("/drivers")
# def driver_report(
#     start_date: date | None = None,
#     end_date: date | None = None,
#     minimum_net: Decimal | None = Query(default=None, ge=0),
#     db: Session = Depends(get_database),
# ):
#     if start_date and end_date and start_date > end_date:
#         raise HTTPException(
#             status_code=400,
#             detail="start_date must not be after end_date",
#         )

#     return get_driver_report(
#         db, start_date, end_date, minimum_net
#     )



# @router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
# def add_driver(data: DriverCreate, 
#                db: Session = Depends(get_database)
#                ):
#     return create_driver(db, data)

# @router.get("/", response_model=list[DriverResponse])
# def list_drivers(db: Session = Depends(get_database)):
#     return get_drivers(db)

# @router.get("/{driver_id}", response_model=DriverResponse)
# def read_driver(driver_id: int, db: Session = Depends(get_database)):
#     return get_driver(db, driver_id)


# @router.get(
#     "/{driver_id}/collections",
#     response_model=DriverWithCollectionsResponse,
# )
# def read_driver_with_collections(
#     driver_id: int,
#     db: Session = Depends(get_database),
# ):
#     return get_driver_with_collection   (db, driver_id)





from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from dependencies.database import get_database
from schemas.driver_schema import (
    DriverCreate,
    DriverResponse,
    DriverWithCollectionsResponse,
)
from services.driver_service import (
    create_driver,
    get_driver,
    get_drivers,
    get_driver_with_collection,
)

router = APIRouter(
    prefix="/api/drivers",
    tags=["Drivers"],
)


@router.post(
    "/",
    response_model=DriverResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_driver(
    data: DriverCreate,
    db: Session = Depends(get_database),
):
    return create_driver(db, data)


@router.get("/", response_model=list[DriverResponse])
def list_drivers(db: Session = Depends(get_database)):
    return get_drivers(db)


@router.get(
    "/{driver_id}/collections",
    response_model=DriverWithCollectionsResponse,
)
def read_driver_with_collections(
    driver_id: int,
    db: Session = Depends(get_database),
):
    return get_driver_with_collection(db, driver_id)


@router.get("/{driver_id}", response_model=DriverResponse)
def read_driver(
    driver_id: int,
    db: Session = Depends(get_database),
):
    return get_driver(db, driver_id)
