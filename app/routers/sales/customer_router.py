from fastapi import APIRouter, HTTPException, status
from typing import List
from app.dependencies.dependencies import CustomerServ, CurrentUser
from app.schemas.sales.customer_schema import CustomerOutSchema, CustomerCreateSchema

router = APIRouter(prefix="/customer", tags=["customer"])

@router.get("/all", response_model=List[CustomerOutSchema])
async def get_all_customers(customer_service: CustomerServ, currentUser: CurrentUser):
    return await customer_service.get_all_customers()

@router.get("/{id_customer}", response_model=CustomerOutSchema)
async def get_customer(id_customer: int, customer_service: CustomerServ, currentUser: CurrentUser):
    result = await customer_service.get_customer(id_customer)
    if not result:         
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.post("", response_model=CustomerOutSchema)
async def create_customer(customer_data: CustomerCreateSchema, customer_service: CustomerServ, currentUser: CurrentUser):
    return await customer_service.create_customer(
        customer_data.CustomerName, customer_data.ContactName, customer_data.Address,
        customer_data.City, customer_data.PostalCode, customer_data.Country
    )

@router.put("/{id_customer}", response_model=CustomerOutSchema)
async def update_customer(id_customer: int, customer_data: CustomerCreateSchema, customer_service: CustomerServ, currentUser: CurrentUser):
    result = await customer_service.update_customer(
        id_customer, customer_data.CustomerName, customer_data.ContactName, customer_data.Address,
        customer_data.City, customer_data.PostalCode, customer_data.Country
    )
    if not result:         
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.delete("/{id_customer}")
async def delete_customer(id_customer: int, customer_service: CustomerServ, currentUser: CurrentUser):
    result = await customer_service.get_customer(id_customer)
    delete = await customer_service.delete_customer(id_customer)
    if not delete:        
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return {"message": f"customer {result.CustomerName} has been deleted"}