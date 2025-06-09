from app.backend.db_model import *
from sqlalchemy import ForeignKey

class OrderDetail(Base):
    __tablename__ = "OrderDetails"
    OrderDetailID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    OrderID: Mapped[int] = mapped_column(ForeignKey("Orders.OrderID"))
    ProductID: Mapped[int] = mapped_column(ForeignKey("Products.ProductID"))
    Quantity: Mapped[int]

    order: Mapped["Order"] = relationship("Order", back_populates="order_details")
    product: Mapped["Product"] = relationship("Product", back_populates="order_details")