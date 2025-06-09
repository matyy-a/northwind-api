from app.backend.db_model import *

class Category(Base):
    __tablename__ = "Categories"
    CategoryID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    CategoryName: Mapped[str] = mapped_column(nullable=False)
    Description: Mapped[str] = mapped_column(nullable=False)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")