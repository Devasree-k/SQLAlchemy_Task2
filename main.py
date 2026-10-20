from fastapi import FastAPI
from database.base import Base
from database.connection import engine

from models.driver_model import Driver
from models.transport_collection_model import TransportCollection
from routers.driver_router import router as driver_router
from routers.transport_collection_router import router as collection_router
from routers.report_router import router as report_router

# Automatically creats database table based on ORM model
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Transport Collection System",
    description="Practice of SQLAlchemy relationships and JOIN ",
    version="1.0.0",
)

app.include_router(report_router)
app.include_router(driver_router)
app.include_router(collection_router)

@app.get("/")
def home():
    return {"message": "Transport Collection System is running"}
