# app/schemas.py
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str


class ItemCreate(BaseModel):
    name: str
    description: str


class ItemUpdate(BaseModel):
    name: str
    description: str


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str


class Item(ItemBase):
    id: int
