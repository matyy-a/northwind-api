from app.backend.db_model import *
from datetime import date

class Employee(Base):
    __tablename__ = "Employees"
    EmployeeID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    LastName: Mapped[str]
    FirstName: Mapped[str]
    BirthDate: Mapped[date]
    Photo: Mapped[str]
    Notes: Mapped[str]

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="employee")