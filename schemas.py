from pydantic import BaseModel


class UserBase(BaseModel):
    phone: str
    first_name: str
    last_name: str


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
    name: str

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    price: int
    discount: int
    description: str
    category_id: str

    class Config:
        orm_mode = True


class Product(BaseModel):
    id: int
    name: str
    price: int
    discount: int
    description: str
    category_id: str

    class Config:
        orm_mode = True
