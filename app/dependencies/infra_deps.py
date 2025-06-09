from redis import Redis
from fastapi import Depends
from typing import Annotated
from app.backend.db_session import get_db_session
from app.repository.user_repository import UserRepository
from app.repository.category_repository import CategoryRepository
from app.repository.supplier_repository import SupplierRepository
from app.repository.customer_repository import CustomerRepository
from app.repository.employee_repository import EmployeeRepository
from app.repository.shipper_repository import ShipperRepository
from app.repository.product_repository import ProductRepository
from app.repository.order_repository import OrderRepository
from app.repository.order_detail_repository import OrderDetailRepository
from app.utils.config import settings
from sqlalchemy.ext.asyncio import AsyncSession

"""
Dependencias para infra
"""

def get_redis_client() -> Redis:
    return Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        #db=settings.redis_db,
        decode_responses=True
    )

def get_user_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserRepository:
    return UserRepository(db_session)

def get_category_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> CategoryRepository:
    return CategoryRepository(db_session)

def get_supplier_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> SupplierRepository:
    return SupplierRepository(db_session)

def get_customer_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> CustomerRepository:
    return CustomerRepository(db_session)

def get_employee_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> EmployeeRepository:
    return EmployeeRepository(db_session)

def get_shipper_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> ShipperRepository:
    return ShipperRepository(db_session)

def get_product_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> ProductRepository:
    return ProductRepository(db_session)

def get_order_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> OrderRepository:
    return OrderRepository(db_session)

def get_order_detail_repository(
    db_session: Annotated[AsyncSession, Depends(get_db_session)]
) -> OrderDetailRepository:
    return OrderDetailRepository(db_session)