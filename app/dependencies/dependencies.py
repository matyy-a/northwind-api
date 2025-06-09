from typing import Annotated
from fastapi import Depends
from app.models.auth.user_model import User
from app.services.auth.security_service import SecurityService
from app.services.auth.token_service import TokenService
from app.services.auth.token_blacklist_service import TokenBlackListService
from app.services.auth.auth_service import AuthService
from app.services.auth.auth_google_service import AuthGoogleService
from app.services.auth.user_service import UserService

from app.services.products.category_service import CategoryService
from app.services.products.supplier_service import SupplierService
from app.services.products.product_service import ProductService
from app.services.sales.customer_service import CustomerService
from app.services.sales.employee_service import EmployeeService
from app.services.sales.shipper_service import ShipperService
from app.services.sales.order_service import OrderService
from app.services.sales.order_detail_service import OrderDetailService

#from app.dependencies.infra_deps import (
#    get_redis_client,
#    get_user_repository,
#    get_category_repository,
#    get_supplier_repository,
#    get_customer_repository,
#)

from app.dependencies.auth_deps import (
    oauth2_scheme,
    get_current_user,
)

from app.dependencies.service_deps import (
    get_security_service,
    get_token_service,
    get_token_blacklist_service,
    get_user_service,
    get_auth_service,
    get_auth_google_service,
    get_category_service,
    get_supplier_service,
    get_customer_service,
    get_employee_service,
    get_shipper_service,
    get_product_service,
    get_order_service,
    get_order_detail_service,
)

# ===== DEPENDENCIAS DE INFRAESTRUCTURA =====
#DbSession = Annotated[AsyncSession, Depends(get_db_session)]
#RedisClient = Annotated[Redis, Depends(get_redis_client)]
#UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
#CategoryRepo = Annotated[CategoryRepository, Depends(get_category_repository)]


# ===== DEPENDENCIAS DE SERVICIOS =====
SecurityServ = Annotated[SecurityService, Depends(get_security_service)]
TokenServ = Annotated[TokenService, Depends(get_token_service)]
TokenBlacklistServ = Annotated[TokenBlackListService, Depends(get_token_blacklist_service)]
UserServ = Annotated[UserService, Depends(get_user_service)]
AuthServ = Annotated[AuthService, Depends(get_auth_service)]
AuthGoogleServ = Annotated[AuthGoogleService, Depends(get_auth_google_service)]
CategoryServ = Annotated[CategoryService, Depends(get_category_service)]
SupplierServ = Annotated[SupplierService, Depends(get_supplier_service)]
CustomerServ = Annotated[CustomerService, Depends(get_customer_service)]
EmployeeServ = Annotated[EmployeeService, Depends(get_employee_service)]
ShipperServ = Annotated[ShipperService, Depends(get_shipper_service)]
ProductServ = Annotated[ProductService, Depends(get_product_service)]
OrderServ = Annotated[OrderService, Depends(get_order_service)]
OrderDetailServ = Annotated[OrderDetailService, Depends(get_order_detail_service)]

# ===== DEPENDENCIAS DE AUTENTICACIÓN =====
TokenDep = Annotated[str, Depends(oauth2_scheme)]
CurrentUser = Annotated[User, Depends(get_current_user)]