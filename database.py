import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.models import Base, Customer, Product

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(_PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "business.db")

os.makedirs(DATA_DIR, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

SEED_PRODUCTS = [
    {"name": "Laptop - Business Pro 14", "category": "Laptops", "unit_price": 45000.0, "stock_quantity": 120, "reorder_level": 20},
    {"name": "Hard Disk - 1TB External", "category": "Storage", "unit_price": 3500.0, "stock_quantity": 500, "reorder_level": 50},
    {"name": "Monitor - 24 inch FHD", "category": "Monitors", "unit_price": 9500.0, "stock_quantity": 75, "reorder_level": 15},
    {"name": "Wireless Mouse", "category": "Accessories", "unit_price": 650.0, "stock_quantity": 300, "reorder_level": 40},
    {"name": "Mechanical Keyboard", "category": "Accessories", "unit_price": 2200.0, "stock_quantity": 90, "reorder_level": 20},
]

SEED_CUSTOMERS = [
    {"name": "Acme Retail Pvt Ltd", "email": "procurement@acmeretail.com", "phone": "+91-9876543210", "lead_status": "New"},
    {"name": "Bluewave Logistics", "email": "purchase@bluewave.com", "phone": "+91-9812345678", "lead_status": "Contacted"},
]


def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        if session.query(Product).count() == 0:
            session.bulk_insert_mappings(Product, SEED_PRODUCTS)
        if session.query(Customer).count() == 0:
            session.bulk_insert_mappings(Customer, SEED_CUSTOMERS)
        session.commit()
    finally:
        session.close()
