#этот файл настроен для запуска в docker контейнере
#необходимо установить на локальном компьютере базу postgreesql и восстановить дамп из dump.sql
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Numeric, BigInteger, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship, joinedload
from pydantic import BaseModel
#from config import settings
from typing import List
#import uvicorn



#connect_str = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
engine = create_engine('postgresql+psycopg2://admin:adminp@host.docker.internal:5432/managesklad')
#engine = create_engine(connect_str, echo=True)
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


class OrderPost(BaseModel):
    datecreate: datetime
    status_id: int
    order_items: list[OrderItemP]


class OrderOut(BaseModel):
    id: int
    datecreate: datetime
    status_id: int

class OrderUpdate(BaseModel):
    status_id: int



app = FastAPI()



@app.get("/")
def root():
    return {"app": "work!!!"}


#эндпоинты для товаров
#,description="Get list products"
@app.get("/products")
def get_all_products():
    '''
    Получение списка продуктов
    * :return: Возврат списка продуктов вместе со статусом выполнения и количеством продуктов
    '''
    db_products = session.query(Product).all()
    if not db_products:
        raise HTTPException(status_code=404, detail="Product not found")
    return {'status': 'success', 'results': len(db_products), 'notes': db_products}


#,description="Get one product"
@app.get("/products/{product_id}")
def get_product(product_id: int):
    '''
    Получение информации о конкретном продукте
    * :param product_id: Уникальные номер продукта
    * :return: Возврат информации о продукте
    '''
    db_product = session.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


#, description="Insert new product"
@app.post("/products", status_code=201)
def create_product(product: ProductP):
    '''
    Добавление нового продукта
    * :param product: Объект, содержащий информацию для добавления
    * :return: Возврат добавленного продукта
    '''
    db_product = Product(**product.dict())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    session.close()
    return db_product

#, description="Update product"
@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductP):
    '''
    Обновление информации о продукте
    * :param product_id: Уникальный номер продукта
    * :param product: Объект, содержащий информацию для обновления
    * :return: Возврат информации о обновленном продукте
    '''
    db_product = session.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    session.commit()
    session.refresh(db_product)
    session.close()
    return db_product


#,description="Delete product"
@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    '''
    Удаление продукта
    * :param product_id: Уникальный номер продукта

    '''
    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    session.close()



#эндпоинты для заказов
#,description="Get list orders"
@app.get("/orders")
def get_all_orders():
    '''
    Получение списка заказов
    * :return: Возврат списка заказав вместе с статусом выполнения и количеством заказов
    '''
    db_orders = session.query(Order).all()
    if not db_orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return {'status': 'success', 'results': len(db_orders), 'notes': db_orders}


#,description="Get one order"
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    '''
    Получение данных заказа с строками
    * :param order_id: Уникальный номер заказа
    * :return:
    '''
    #db_order = session.query(Order).filter(Order.id == order_id).first()
    db_order = session.query(Order).options(joinedload(Order.order_items)).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


#,  description="Insert new order"
@app.post("/orders", response_model=OrderPost)
def create_order(order: OrderPost):
    '''
    Создание нового заказа
    * :param order: Данные нового заказа
    * :return: Возврат заказа вместе с строками
    '''
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
        return order


#, description="Update order status"
@app.put("/orders/{order_id}", response_model=OrderOut)
def update_orderstatus(order_id: int, order: OrderUpdate) : #-> OrderBase
    '''
    Обновление статуса заказа
    * :param order_id: Уникальный номер заказа
    * :param order: Поля заказа
    * :return: Возврат обновленного заказа
    '''
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
        db_order = session.query(Order).filter(Order.id == order_id).first()
        session.close()
        return db_order
