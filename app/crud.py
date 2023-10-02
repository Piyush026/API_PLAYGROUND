from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from . import models
from . import schemas


def create_item(db: Session, item_data):
    try:
        db_item = models.Item(**item_data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError:  # Catch IntegrityError
        raise HTTPException(status_code=400, detail="Name already exist")


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_all_item(db: Session, skip: int = 0, limit: int = 100):
    items = db.query(models.Item).offset(skip).limit(limit).all()
    db.close()
    return items


def update_item(db: Session, item_id: int, item_data: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        for key, value in item_data.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
