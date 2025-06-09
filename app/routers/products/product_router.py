from fastapi import APIRouter, HTTPException, status
from typing import List
from app.dependencies.dependencies import ProductServ, CurrentUser
from app.schemas.products.product_schema import ProductOutSchema, ProductCreateSchema

router = APIRouter(prefix="/product", tags=["product"])

@router.get("/all", response_model=List[ProductOutSchema])
async def get_all_products(product_service: ProductServ, currentUser: CurrentUser):
    return await product_service.get_all_products()

@router.get("/{id_product}", response_model=ProductOutSchema)
async def get_product(id_product: int, product_service: ProductServ, currentUser: CurrentUser):
    result = await product_service.get_product(id_product)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.post("", response_model=ProductOutSchema)
async def create_product(product_data: ProductCreateSchema, product_service: ProductServ, currentUser: CurrentUser):
    result = await product_service.create_product(
        product_data.ProductName, product_data.SupplierID, product_data.CategoryID,
        product_data.Unit, product_data.Price
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.put("/{id_product}", response_model=ProductOutSchema)
async def update_product(id_product: int, product_data: ProductCreateSchema, product_service: ProductServ, currentUser: CurrentUser):
    result = await product_service.update_product(
        id_product, product_data.ProductName, product_data.SupplierID, product_data.CategoryID,
        product_data.Unit, product_data.Price
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.delete("/{id_product}")
async def delete_product(id_product: int, product_service: ProductServ, currentUser: CurrentUser):
    result = await product_service.get_product(id_product)
    delete = await product_service.delete_product(id_product)
    if not delete:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return {"message": f"product {result.ProductName} has been deleted"}