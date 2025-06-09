from app.backend.db_model import *

class Customer(Base):
    __tablename__ = "Customers"
    CustomerID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    CustomerName: Mapped[str]
    ContactName: Mapped[str]
    Address: Mapped[str]
    City: Mapped[str]
    PostalCode: Mapped[str]
    Country: Mapped[str]

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="customer")