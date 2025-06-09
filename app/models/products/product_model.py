from app.backend.db_model import *
from sqlalchemy import ForeignKey

class Product(Base):
    __tablename__ = "Products"
    ProductID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ProductName: Mapped[str]
    SupplierID: Mapped[int] = mapped_column(ForeignKey("Suppliers.SupplierID"))
    CategoryID: Mapped[int] = mapped_column(ForeignKey("Categories.CategoryID"))
    Unit: Mapped[str]
    Price: Mapped[float] = mapped_column(default=0)

    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="products")
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    order_details: Mapped[list["OrderDetail"]] = relationship("OrderDetail", back_populates="product")