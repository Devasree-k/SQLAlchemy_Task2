
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies.database import get_database
from services.driver_service import get_driver_report

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)


@router.get("/drivers")
def driver_report(
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_database),
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must not be after end_date",
        )

    return get_driver_report(db, start_date, end_date)
