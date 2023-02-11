from typing import Optional
from urllib.request import Request

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User, tags=['user'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User], tags=['user'])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=['user'])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{item_id}", response_model=schemas.User, tags=['user'])
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user:
        return crud.update_user(db=db, user_id=user_id, user=user)
    raise HTTPException(status_code=400, detail="user is not registered")


@app.get("/category/", response_model=list[schemas.Category], tags=['category'])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_categories(db, skip=skip, limit=limit)
    return categories


@app.get("/category/{category_id}", response_model=schemas.Category, tags=['category'])
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.post("/category/", response_model=schemas.Category, tags=['category'])
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    db_category = crud.get_category_by_name(db, name=category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already registered")
    return crud.create_category(db=db, category=category)


@app.put("/category/{category_id}", response_model=schemas.Category, tags=['category'])
def update_category(category_id: int, category: schemas.CategoryBase, db: Session = Depends(get_db)):
    db_category = crud.get_category(db, category_id=category_id)
    if db_category:
        return crud.update_category(db=db, category_id=category_id, category=category)
    raise HTTPException(status_code=400, detail="user is not registered")


@app.post("/product/", response_model=schemas.Product, tags=['product'])
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already registered")
    return crud.create_product(db=db, product=product)


@app.get("/product/", response_model=list[schemas.Product], tags=['product'])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_products(db, skip=skip, limit=limit)
    return categories


@app.get("/product/{product_id}", response_model=schemas.Product, tags=['product'])
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_product


@app.put("/products/{item_id}", response_model=schemas.Product, tags=['product'])
def update_product(product_id: int, product: schemas.ProductBase, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product:
        return crud.update_product(db=db, product_id=product_id, product=product)
    raise HTTPException(status_code=400, detail="product is not registered")


@app.get("/product/search/", response_model=schemas.Product, tags=['product'])
def search(query: Optional[str] = None, db: Session = Depends(get_db)):
    print("111111111111111111", query)
    if query:
        return crud.search_product(query=query, db=db)
    HTTPException(status_code=404, detail="product is not found")
