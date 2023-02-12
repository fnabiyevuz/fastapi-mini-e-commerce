from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    phone: str
    first_name: str
    last_name: str
    status: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    price: int
    quantity: int
    discount: int
    description: str
    category_id: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    id: int
    name: str
    quantity: int
    price: int
    discount: int
    description: str
    category_id: str

    class Config:
        orm_mode = True


class ShopBase(BaseModel):
    user: int
    created_date: datetime
    status: str

    class Config:
        orm_mode = True


class ShopCreate(BaseModel):
    user: int

    class Config:
        orm_mode = True


class ShopStatus(BaseModel):
    status: str

    class Config:
        orm_mode = True


class Shop(ShopBase):
    id: int
    status: str

    class Config:
        orm_mode = True


class ShopItemBase(BaseModel):
    shop: int
    product: int
    quantity: int

    class Config:
        orm_mode = True


class ShopItem(ShopItemBase):
    id: int

    class Config:
        orm_mode = True
