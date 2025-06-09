from app.backend.db_model import *

class Shipper(Base):
    __tablename__ = "Shippers"
    ShipperID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ShipperName: Mapped[str]
    Phone: Mapped[str]

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="shipper")