from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from dependencies.database import get_database
from schemas.transport_collection_schema import (
    CollectionCreate, CollectionUpdate, CollectionResponse
)
from services.transport_collection_service import (
    create_collection, get_collections, get_collection,
    update_collection, delete_collection,
)

router = APIRouter(prefix="/api/collections", tags=["Transport Collections"])

@router.post("/", response_model=CollectionResponse, status_code=status.HTTP_201_CREATED)
def add_collection(data: CollectionCreate, db: Session = Depends(get_database)):
    return create_collection(db, data)

@router.get("/", response_model=list[CollectionResponse])
def list_collections(db: Session = Depends(get_database)):
    return get_collections(db)

@router.get("/{collection_id}", response_model=CollectionResponse)
def read_collection(collection_id: int, db: Session = Depends(get_database)):
    return get_collection(db, collection_id)

@router.patch("/{collection_id}", response_model=CollectionResponse)
def edit_collection(collection_id: int, data: CollectionUpdate, db: Session = Depends(get_database)):
    return update_collection(
        db, collection_id, data.model_dump(exclude_unset=True)
    )

@router.delete("/{collection_id}")
def remove_collection(collection_id: int, db: Session = Depends(get_database)):
    return delete_collection(db, collection_id)
