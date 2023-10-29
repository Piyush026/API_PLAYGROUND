from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.items import crud
from app.items.crud import get_post_and_check_ownership
from app.items.schemas import ItemCreate, ItemResponse, ItemUpdate

import logging

from app.users_app import schemas
from app.users_app.oauth2 import get_current_user
from database import get_db

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/create/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(get_current_user)):
    db_item = crud.create_item(db, item.dict(), owner_id=current_user.username)
    return db_item


@router.get("/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    try:
        item = crud.get_item(db, item_id)
        return ItemResponse(**item.__dict__)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid value")
    except AttributeError:
        raise HTTPException(status_code=404, detail="Key not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db),
                db_item: ItemUpdate = Depends(get_post_and_check_ownership)):
    try:
        db_item = crud.update_item(db, item_id, item)
        return ItemResponse(**db_item.__dict__)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db),
                db_item: ItemUpdate = Depends(get_post_and_check_ownership)):
    try:
        db_item = crud.delete_item(db, item_id)
        return ItemResponse(**db_item.__dict__)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all/", response_model=List[ItemResponse])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        items = crud.get_all_item(db, skip, limit)
        return [ItemResponse(**item.__dict__) for item in items]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid value")
    except AttributeError:
        raise HTTPException(status_code=404, detail="Key not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
