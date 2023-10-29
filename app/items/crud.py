from fastapi import HTTPException, Depends, status,Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.items import models, schemas
from app.users_app.oauth2 import get_current_user
from database import get_db
from app.users_app import schemas as user_schemas


def create_item(db: Session, item_data, owner_id):
    try:
        db_item = models.Item(**item_data, owner_id=owner_id)
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


def get_post_and_check_ownership(item_id: int, db: Session = Depends(get_db),
                                 current_user: user_schemas.User = Depends(get_current_user),
                                 request: Request = None):
    db_item = get_item(db, item_id)
    operation_type = request.method
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if operation_type == "PUT" and db_item.owner_id != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this Item")
    elif operation_type == "DELETE" and db_item.owner_id != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this Item")
    return db_item

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
