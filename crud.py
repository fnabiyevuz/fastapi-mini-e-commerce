from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(phone=user.phone, password=user.password, first_name=user.first_name,
                          last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    db_user.phone = user.phone
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.password = user.password

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.CategoryBase):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category: schemas.UserCreate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()

    db_category.name = category.name

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()


def create_product(db: Session, product: schemas.ProductBase):
    db_product = models.Product(name=product.name, price=product.price, discount=product.discount,
                                description=product.description, category_id=product.category_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def update_product(db: Session, product_id: int, product: schemas.ProductBase):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    db_product.name = product.name
    db_product.price = product.price
    db_product.discount = product.discount
    db_product.description = product.description
    db_product.category_id = product.category_id

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def search_product(query: str, db: Session):
    print('query', query)
    products = db.query(models.Product).filter(models.Product.name.contains(query)).all()
    return products
