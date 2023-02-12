from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini E-commerce API", version="1.0")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/sts/{status}", response_model=list[schemas.User], tags=['user'])
def by_sts(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if status:
        return crud.by_status(db=db, status=status)
    raise HTTPException(status_code=400, detail="Status is not registered")


@app.get("/users/{user_id}", response_model=schemas.User, tags=['user'])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=list[schemas.User], tags=['user'])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/", response_model=schemas.User, tags=['user'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.put("/users/{item_id}", response_model=schemas.User, tags=['user'])
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user:
        return crud.update_user(db=db, user_id=user_id, user=user)
    raise HTTPException(status_code=400, detail="user is not registered")

@app.delete("/users/{users_id}", tags=["user"])
def delete_users(users_id: int):
    with Session(engine) as session:
        item = session.get(models.User, users_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return {"ok": True}

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

@app.delete("/category/{category_id}", tags=["category"])
def delete_category(category_id: int):
    with Session(engine) as session:
        item = session.get(models.Category, category_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return {"ok": True}

@app.get("/product/", response_model=list[schemas.Product], tags=['product'])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud.get_products(db, skip=skip, limit=limit)
    return categories


@app.get("/product/search/", response_model=schemas.Product, tags=['product'])
def search(query: Optional[str] = None, db: Session = Depends(get_db)):
    if query:
        return crud.search_product(query=query, db=db)
    HTTPException(status_code=404, detail="product is not found")


@app.get("/product/{product_id}", response_model=schemas.Product, tags=['product'])
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_product


@app.post("/product/", response_model=schemas.Product, tags=['product'])
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_name(db, name=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already registered")
    return crud.create_product(db=db, product=product)


@app.put("/products/{item_id}", response_model=schemas.Product, tags=['product'])
def update_product(product_id: int, product: schemas.ProductBase, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product:
        return crud.update_product(db=db, product_id=product_id, product=product)
    raise HTTPException(status_code=400, detail="product is not registered")

@app.delete("/product/{product_id}", tags=["product"])
def delete_product(product_id: int):
    with Session(engine) as session:
        item = session.get(models.Product, product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return {"ok": True}


@app.get("/shops/{shop_id}", response_model=schemas.Shop, tags=['shop'])
def read_shop(shop_id: int, db: Session = Depends(get_db)):
    db_shop = crud.get_shop(db, shop_id=shop_id)
    if db_shop is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_shop


@app.get("/shops/", response_model=list[schemas.Shop], tags=['shop'])
def read_shops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shops = crud.get_shops(db, skip=skip, limit=limit)
    return shops


@app.post("/shop/", response_model=schemas.Shop, tags=['shop'])
def create_shop(shop: schemas.ShopCreate, db: Session = Depends(get_db)):
    db_shop = crud.get_shop_by_user(db, user=shop.user, status="opened")
    if db_shop:
        raise HTTPException(status_code=400, detail="Shop already created")
    return crud.create_shop(db=db, shop=shop)


@app.get("/shops/sts/{status}", response_model=list[schemas.Shop], tags=['shop'])
def filter_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if status:
        return crud.shop_by_status(db=db, status=status)
    raise HTTPException(status_code=400, detail="Status is not found")


@app.put("/shops/change_sts/", response_model=schemas.Shop, tags=['shop'])
def change_status(shop_id: int, status: str, db: Session = Depends(get_db)):
    if status:
        return crud.shop_change_status(db=db, status=status, shop_id=shop_id)
    raise HTTPException(status_code=400, detail="Status is not found")

@app.delete("/shop/{shop_id}", tags=["shop"])
def delete_shop(shop_id: int):
    with Session(engine) as session:
        item = session.get(models.Shop, shop_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return {"ok": True}

@app.get("/shopitem/{shopitem_id}", response_model=schemas.ShopItem, tags=['shopitem'])
def read_shopitem(shopitem_id: int, db: Session = Depends(get_db)):
    db_shopitem = crud.get_shopitem(db, shopitem_id=shopitem_id)
    if db_shopitem is None:
        raise HTTPException(status_code=404, detail="ShopItem not found")
    return db_shopitem


@app.get("/shopitem/", response_model=list[schemas.ShopItem], tags=['shopitem'])
def read_shopitems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    shopitems = crud.get_shopitems(db, skip=skip, limit=limit)
    return shopitems
@app.post("/shopitem/", response_model=schemas.ShopItem, tags=['shopitem'])
def create_shopitem(shopitem: schemas.ShopItemBase, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_product_shop(db, shopitem=shopitem)
    if db_item:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_item(db=db, shopitem=shopitem)


@app.put("/shopitem/change_quan/", response_model=schemas.ShopItem, tags=['shopitem'])
def update_quantity(shopitem_id: int, quantity: int, db: Session = Depends(get_db)):
    if quantity and shopitem_id:
        return crud.shopitem_upd_quan(db=db, quantity=quantity, shopitem_id=shopitem_id)
    raise HTTPException(status_code=400, detail="Status or Shop are not found")


@app.delete("/shopitem/{item_id}", tags=["shopitem"])
def delete_shopitem(item_id: int):
    with Session(engine) as session:
        item = session.get(models.ShopItem, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return {"ok": True}