from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Numeric, BigInteger, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship, joinedload
from pydantic import BaseModel
from config import settings
from typing import List
import uvicorn



connect_str = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
#engine = create_engine('postgresql+psycopg2://admin:adminp@localhost:5432/managesklad')
engine = create_engine(connect_str, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()


#модели таблиц
#названия таблиц и полей должны соблюдать регистр написания

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prodname = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Float, nullable=False)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    datecreate = Column(DateTime, nullable=False)
    status_id = Column(Integer, ForeignKey('statuses.id'))
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "ordersitems"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Float)
    order = relationship("Order", back_populates="order_items")

class Status(Base):
    __tablename__ = "statuses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    statusname = Column(String, nullable=False)


#создание таблиц
#Base.metadata.create_all(bind=engine)


#Модели pydantic

class ProductP(BaseModel):
    prodname: str
    description: str
    price: float
    stock: float



class OrderItemP(BaseModel):
    product_id: int
    quantity: float


class OrderP(BaseModel):
    datecreate: datetime
    status_id: int
    order_items: list[OrderItemP]

class OrderUpdate(BaseModel):
    status_id: int


app = FastAPI()



@app.get("/")
async def root():
    return {"app": "work!!!"}


#эндпоинты для товаров

@app.get("/products",description="Get list products")
def get_all_products():
    db_products = session.query(Product).all()
    if not db_products:
        raise HTTPException(status_code=404, detail="Product not found")
    return {'status': 'success', 'results': len(db_products), 'notes': db_products}



@app.get("/products/{product_id}",description="Get one product")
def get_product(product_id: int):
    db_product = session.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product



@app.post("/products", status_code=201, description="Insert new product")
def create_product(product: ProductP):
    db_product = Product(**product.dict())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    session.close()
    return db_product


@app.put("/products/{product_id}", description="Update product")
def update_product(product_id: int, product: ProductP):
    db_product = session.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    session.commit()
    session.refresh(db_product)
    session.close()
    return db_product



@app.delete("/products/{product_id}",description="Delete product", status_code=204)
def delete_product(product_id: int):
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    session.close()



#эндпоинты для заказов

@app.get("/orders",description="Get list orders")
def get_all_orders():
    db_orders = session.query(Order).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return {'status': 'success', 'results': len(db_orders), 'notes': db_orders}



@app.get("/orders/{order_id}",description="Get one order")
def get_order(order_id: int):
    #db_order = session.query(Order).filter(Order.id == order_id).first()
    db_order = session.query(Order).options(joinedload(Order.order_items)).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order



@app.post("/orders",  description="Insert new order")
def create_order(order: OrderP):
    #проверим данные на корректность перед вставкой
    errors_list = []

    db_statusid = session.query(Status).filter(Status.id == order.status_id).first()
    if not db_statusid:
        errors_list.append( 'Status id = ' + str(order.status_id) + ' not found')
    
    for item in order.order_items:
        db_product = session.query(Product).filter(Product.id == item.product_id).first()
        if not db_product:
            errors_list.append('Product id = '+str(item.product_id)+' not found')
        else:
            if item.quantity > db_product.stock:
                errors_list.append('Product id = ' + str(item.product_id)  + ', Product name = ' + db_product.prodname +',  There is not enough product! (stock =  ' + str(db_product.stock) + ' < in order =  ' + str(item.quantity) + ')')

    if errors_list.__len__() > 0:
        return { "details":"order not save!",  "errors": errors_list}
    else:
        #выполняем вставку
        #реализация логики с количеством
        new_order = Order(datecreate=order.datecreate, status_id=order.status_id)
        session.add(new_order)
        session.commit()
        session.refresh(new_order)

        for item in order.order_items:
            new_order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
            session.add(new_order_item)
            db_product = session.query(Product).filter(Product.id == item.product_id).first()
            db_product.stock = db_product.stock - item.quantity

        session.commit()
        session.close()
        return new_order



@app.put("/orders/{order_id}", description="Update order status")
def update_orderstatus(order_id: int, order: OrderUpdate):
    errors_list = []
    db_status = session.query(Status).filter(Status.id == order.status_id).first()
    if not db_status:
        errors_list.append('Status id = ' + str(order.status_id) + ' not found')
    db_order = session.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        errors_list.append('Order id = ' + str(order_id) + ' not found')
    if errors_list.__len__() > 0:
        return { "details":"order not save!",  "errors": errors_list}
    else:
        # обновляем статус
        db_order.status_id = order.status_id
        session.commit()
        session.close()
        return db_order



if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="localhost", log_level="info")