from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime
from database import Base
from sqlalchemy_utils.types.choice import ChoiceType


class User(Base):
    __tablename__ = "users"
    sts = (
        ("client", "client"),
        ("call_center", "call_center"),
        ("manager", "manager"),
        ("deliver", "deliver"),
        ("cashier", "cashier"),
    )
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    status = Column(String, ChoiceType(sts), default="clients")

    shop_s = relationship("Shop", back_populates="user_s")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    product_s = relationship("Product", back_populates="category_s")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer, default=0)
    price = Column(Integer)
    discount = Column(Integer, default=0)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category_s = relationship("Category", back_populates="product_s")
    product_sh = relationship("ShopItem", back_populates="shopitem_p")


class Shop(Base):
    __tablename__ = "shops"
    sts = (
        ("opened", "opened"),
        ("booked", "booked"),
        ("canceled", "canceled"),
        ("accepted", "accepted"),
        ("sent", "sent"),
        ("sold", "sold"),
        ("paid", "paid"),
    )
    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("users.id"))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, ChoiceType(sts), default="opened")

    user_s = relationship("User", back_populates="shop_s")
    shopitem_sh = relationship("ShopItem", back_populates="shop_sh")


class ShopItem(Base):
    __tablename__ = "itemshop"

    id = Column(Integer, primary_key=True, index=True)
    shop = Column(Integer, ForeignKey("shops.id"))
    product = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

    shop_sh = relationship("Shop", back_populates="shopitem_sh")
    shopitem_p = relationship("Product", back_populates="product_sh")


