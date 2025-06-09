from fastapi import Depends
from redis import Redis
from typing import Annotated
from app.repository.user_repository import UserRepository
from app.repository.category_repository import CategoryRepository
from app.repository.supplier_repository import SupplierRepository
from app.repository.customer_repository import CustomerRepository
from app.repository.employee_repository import EmployeeRepository
from app.repository.shipper_repository import ShipperRepository
from app.repository.product_repository import ProductRepository
from app.repository.order_repository import OrderRepository
from app.repository.order_detail_repository import OrderDetailRepository
from app.services.auth.security_service import SecurityService
from app.services.auth.token_service import TokenService
from app.services.auth.token_blacklist_service import TokenBlackListService
from app.services.auth.auth_service import AuthService
from app.services.auth.auth_google_service import AuthGoogleService
from app.services.auth.user_service import UserService
from app.services.products.category_service import CategoryService
from app.services.products.supplier_service import SupplierService
from app.services.sales.customer_service import CustomerService
from app.services.sales.employee_service import EmployeeService
from app.services.sales.shipper_service import ShipperService
from app.services.products.product_service import ProductService
from app.services.sales.order_service import OrderService
from app.services.sales.order_detail_service import OrderDetailService
from app.utils.config import settings
from app.dependencies.infra_deps import (
    get_redis_client, 
    get_user_repository, 
    get_category_repository, 
    get_supplier_repository,
    get_customer_repository,
    get_employee_repository,
    get_shipper_repository,
    get_product_repository,
    get_order_repository,
    get_order_detail_repository,
)

"""
Dependencias para servicios
"""

def get_security_service() -> SecurityService:
    return SecurityService()

def get_token_blacklist_service(
    redis_client: Annotated[Redis, Depends(get_redis_client)]
) -> TokenBlackListService:
    return TokenBlackListService(redis_client)

def get_token_service(
    blacklist_service: Annotated[TokenBlackListService, Depends(get_token_blacklist_service)]
) -> TokenService:
    return TokenService(
        secret_key=settings.secret_key,
        algorithm=settings.algorithm,
        expire_minutes=settings.access_token_expire_minutes,
        blacklist_service=blacklist_service
    )

def get_user_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    security_service: Annotated[SecurityService, Depends(get_security_service)]
) -> UserService:
    return UserService(user_repository, security_service)

def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    security_service: Annotated[SecurityService, Depends(get_security_service)],
    token_service: Annotated[TokenService, Depends(get_token_service)]
) -> AuthService:
    return AuthService(user_repository, security_service, token_service)

def get_auth_google_service(
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    token_service: Annotated[TokenService, Depends(get_token_service)]
) -> AuthGoogleService:
    return AuthGoogleService(redis_client, auth_service, user_service, token_service)

def get_category_service(
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)]
) -> CategoryService:
    return CategoryService(category_repository)

def get_supplier_service(
    supplier_repository: Annotated[SupplierRepository, Depends(get_supplier_repository)]
) -> SupplierService:
    return SupplierService(supplier_repository)

def get_customer_service(
    customer_repository: Annotated[CustomerRepository, Depends(get_customer_repository)]
) -> CustomerService:
    return CustomerService(customer_repository)

def get_employee_service(
    employee_repository: Annotated[EmployeeRepository, Depends(get_employee_repository)]
) -> EmployeeService:
    return EmployeeService(employee_repository)

def get_shipper_service(
    shipper_repository: Annotated[ShipperRepository, Depends(get_shipper_repository)]
) -> ShipperService:
    return ShipperService(shipper_repository)

def get_product_service(
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
    supplier_repository: Annotated[SupplierRepository, Depends(get_supplier_repository)],
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)]
) -> ProductService:
    return ProductService(product_repository, supplier_repository, category_repository)

def get_order_service(
    order_repository: Annotated[OrderRepository, Depends(get_order_repository)],
    customer_repository: Annotated[CustomerRepository, Depends(get_customer_repository)],
    employee_repository: Annotated[EmployeeRepository, Depends(get_employee_repository)],
    shipper_repository: Annotated[ShipperRepository, Depends(get_shipper_repository)]
) -> OrderService:
    return OrderService(order_repository, customer_repository, employee_repository, shipper_repository)

def get_order_detail_service(
    order_detail_repository: Annotated[OrderDetailRepository, Depends(get_order_detail_repository)],
    order_repository: Annotated[OrderRepository, Depends(get_order_repository)],
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)]
) -> OrderDetailService:
    return OrderDetailService(order_detail_repository, order_repository, product_repository)