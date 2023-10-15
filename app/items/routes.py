from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.items import crud
from app.items.database import get_db
from app.items.schemas import ItemCreate, ItemResponse, ItemUpdate

import logging

router = APIRouter()


logger = logging.getLogger(__name__)

@router.post("/create/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = crud.create_item(db, item.dict())
    return db_item
# raise HTTPException(status_code=400, detail="Internal server error")


# Define other item-related endpoints here

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
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    try:
        db_item = crud.update_item(db, item_id, item)
        return ItemResponse(**db_item.__dict__)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid value")
    except AttributeError:
        raise HTTPException(status_code=404, detail="Key not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try:
        db_item = crud.delete_item(db, item_id)
        return ItemResponse(**db_item.__dict__)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid value")
    except AttributeError:
        raise HTTPException(status_code=404, detail="Key not found")
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
