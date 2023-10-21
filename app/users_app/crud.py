from sqlalchemy.orm import Session
from app.users_app import models, schemas
from app.users_app.token import get_password_hash


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_data: dict):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
