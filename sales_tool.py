from crewai.tools import tool

from backend.db.database import SessionLocal
from backend.db.models import Product


@tool("Generate Sales Quotation")
def generate_quotation(product_name: str, quantity: int, discount_percent: float = 0.0) -> str:
    """Generate a price quotation for a given product name and quantity, applying
    an optional discount percentage (0-100). Verifies stock availability first."""
    session = SessionLocal()
    try:
        product = session.query(Product).filter(Product.name.ilike(f"%{product_name}%")).first()
        if not product:
            return f"Cannot generate quotation: no product found matching '{product_name}'."
        if quantity <= 0:
            return "Quantity must be greater than zero."

        stock_note = ""
        if quantity > product.stock_quantity:
            stock_note = (
                f" WARNING: requested quantity ({quantity}) exceeds current stock "
                f"({product.stock_quantity}); partial fulfillment or backorder required."
            )

        subtotal = product.unit_price * quantity
        discount_amount = subtotal * (discount_percent / 100.0)
        total = subtotal - discount_amount

        return (
            f"Quotation for {quantity} x {product.name}:\n"
            f"Unit Price: Rs.{product.unit_price:,.2f}\n"
            f"Subtotal: Rs.{subtotal:,.2f}\n"
            f"Discount ({discount_percent}%): -Rs.{discount_amount:,.2f}\n"
            f"Total: Rs.{total:,.2f}\n"
            f"Stock available: {product.stock_quantity} units.{stock_note}"
        )
    finally:
        session.close()
