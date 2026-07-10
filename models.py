from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String)
    unit_price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, default=10)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    lead_status = Column(String, default="New")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="Quotation Sent")
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer")
    product = relationship("Product")
