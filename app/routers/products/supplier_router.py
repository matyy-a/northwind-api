from fastapi import APIRouter, HTTPException, status
from typing import List
from app.dependencies.dependencies import SupplierServ, CurrentUser
from app.schemas.products.supplier_schema import SupplierOutSchema, SupplierCreateSchema

router = APIRouter(prefix="/supplier", tags=["supplier"])

@router.get("/all", response_model=List[SupplierOutSchema])
async def get_all_suppliers(supplier_service: SupplierServ, currentUser: CurrentUser):
    return await supplier_service.get_all_suppliers()

@router.get("/{id_supplier}", response_model=SupplierOutSchema)
async def get_supplier(id_supplier: int, supplier_service: SupplierServ, currentUser: CurrentUser):
    result = await supplier_service.get_supplier(id_supplier)
    if not result:         
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.post("", response_model=SupplierOutSchema)
async def create_supplier(supplier_data: SupplierCreateSchema, supplier_service: SupplierServ, currentUser: CurrentUser):
    return await supplier_service.create_supplier(
        supplier_data.SupplierName, supplier_data.ContactName, supplier_data.Address,
        supplier_data.City, supplier_data.PostalCode, supplier_data.Country, supplier_data.Phone
    )

@router.put("/{id_supplier}", response_model=SupplierOutSchema)
async def update_supplier(id_supplier: int, supplier_data: SupplierCreateSchema, supplier_service: SupplierServ, currentUser: CurrentUser):
    result = await supplier_service.update_supplier(
        id_supplier, supplier_data.SupplierName, supplier_data.ContactName, supplier_data.Address,
        supplier_data.City, supplier_data.PostalCode, supplier_data.Country, supplier_data.Phone
    )
    if not result:         
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.delete("/{id_supplier}")
async def delete_supplier(id_supplier: int, supplier_service: SupplierServ, currentUser: CurrentUser):
    result = await supplier_service.get_supplier(id_supplier)
    delete = await supplier_service.delete_supplier(id_supplier)
    if not delete:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return {"message": f"supplier {result.SupplierName} has been deleted"}