from crewai.tools import tool

from backend.db.database import SessionLocal
from backend.db.models import Product


@tool("Check Inventory Stock")
def check_inventory_stock(product_name: str) -> str:
    """Look up the current stock quantity and unit price for a product by name
    (partial match allowed) in the business inventory database."""
    session = SessionLocal()
    try:
        product = session.query(Product).filter(Product.name.ilike(f"%{product_name}%")).first()
        if not product:
            return (
                f"No product found matching '{product_name}'. "
                "Available categories: Laptops, Storage, Monitors, Accessories."
            )
        return (
            f"Product: {product.name} | Category: {product.category} | "
            f"In Stock: {product.stock_quantity} units | Unit Price: Rs.{product.unit_price:,.2f} | "
            f"Reorder Level: {product.reorder_level}"
        )
    finally:
        session.close()
