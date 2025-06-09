from app.backend.db_model import *

class Supplier(Base):
    __tablename__ = "Suppliers"
    SupplierID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    SupplierName: Mapped[str]
    ContactName: Mapped[str]
    Address: Mapped[str]
    City: Mapped[str]
    PostalCode: Mapped[str]
    Country: Mapped[str]
    Phone: Mapped[str]

    products: Mapped[list["Product"]] = relationship("Product", back_populates="supplier")