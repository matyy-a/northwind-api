from app.backend.db_model import *
from sqlalchemy import ForeignKey
from datetime import datetime

class Order(Base):
    __tablename__ = "Orders"
    OrderID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    CustomerID: Mapped[int] = mapped_column(ForeignKey("Customers.CustomerID"))
    EmployeeID: Mapped[int] = mapped_column(ForeignKey("Employees.EmployeeID"))
    OrderDate: Mapped[datetime]
    ShipperID: Mapped[int] = mapped_column(ForeignKey("Shippers.ShipperID"))

    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="orders")
    shipper: Mapped["Shipper"] = relationship("Shipper", back_populates="orders")
    order_details: Mapped[list["OrderDetail"]] = relationship("OrderDetail", back_populates="order")