from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from app.backend.db_session import get_engine
from app.backend.db_model import Base
from app.routers.auth.user_router import router as user_router
from app.routers.auth.auth_router import router as auth_router
from app.routers.products.category_router import router as category_router
from app.routers.products.supplier_router import router as supplier_router
from app.routers.products.product_router import router as product_router
from app.routers.sales.customer_router import router as customer_router
from app.routers.sales.employee_router import router as employee_router
from app.routers.sales.shipper_router import router as shipper_router
from app.routers.sales.order_router import router as order_router
from app.routers.sales.order_detail_router import router as order_detail_router
from app.dependencies.dependencies import CurrentUser

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(supplier_router)
app.include_router(customer_router)
app.include_router(employee_router)
app.include_router(shipper_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(order_detail_router)

@app.get("/hola")
async def homepage(user: CurrentUser):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No estás autorizado"
        )
    return {"Hola": f"{user.username}"}

@app.get("/")
async def root():
    return {"Mi api": "funciona"}

