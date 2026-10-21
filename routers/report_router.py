from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database import get_database
from services.driver_service import DriverService


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)


def get_report_service(
    db: AsyncSession = Depends(get_database),
) -> DriverService:
    return DriverService(db)


@router.get("/drivers")
async def driver_report(
    start_date: date | None = None,
    end_date: date | None = None,
    service: DriverService = Depends(get_report_service),
):
    if (
        start_date is not None
        and end_date is not None
        and start_date > end_date
    ):
        raise HTTPException(
            status_code=400,
            detail="start_date must not be after end_date",
        )

    return await service.get_driver_report(
        start_date,
        end_date,
    )
