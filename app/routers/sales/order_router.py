from fastapi import APIRouter, HTTPException, status
from typing import List
from app.dependencies.dependencies import OrderServ, CurrentUser
from app.schemas.sales.order_schema import OrderOutSchema, OrderCreateSchema

router = APIRouter(prefix="/order", tags=["order"])

@router.get("/all", response_model=List[OrderOutSchema])
async def get_all_orders(order_service: OrderServ, currentUser: CurrentUser):
    return await order_service.get_all_orders()

@router.get("/{order_id}", response_model=OrderOutSchema)
async def get_order(order_id: int, order_service: OrderServ, currentUser: CurrentUser):
    result = await order_service.get_order(order_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return result

@router.post("", response_model=OrderOutSchema)
async def create_order(order_data: OrderCreateSchema, order_service: OrderServ, currentUser: CurrentUser):
    result = await order_service.create_order(
        order_data.CustomerID, order_data.EmployeeID, 
        order_data.OrderDate, order_data.ShipperID
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return result

@router.put("/{order_id}", response_model=OrderOutSchema)
async def update_order(order_id: int, order_data: OrderCreateSchema, order_service: OrderServ, currentUser: CurrentUser):
    result = await order_service.update_order(
        order_id, order_data.CustomerID, order_data.EmployeeID,
        order_data.OrderDate, order_data.ShipperID
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return result

@router.delete("/{order_id}")
async def delete_order(order_id: int, order_service: OrderServ, currentUser: CurrentUser):
    order = await order_service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    
    delete_result = await order_service.delete_order(order_id)
    if not delete_result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return {"message": f"order {order.OrderID} has been deleted"}