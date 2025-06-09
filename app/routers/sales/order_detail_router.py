from fastapi import APIRouter, HTTPException, status
from typing import List
from app.dependencies.dependencies import OrderDetailServ, CurrentUser
from app.schemas.sales.order_schema import OrderDetailOutSchema, OrderDetailCreateSchema

router = APIRouter(prefix="/order-detail", tags=["order-detail"])

@router.get("/all", response_model=List[OrderDetailOutSchema])
async def get_all_order_details(order_detail_service: OrderDetailServ, currentUser: CurrentUser):
    return await order_detail_service.get_all_order_details()

@router.get("/order/{order_id}", response_model=List[OrderDetailOutSchema])
async def get_order_details_by_order(order_id: int, order_detail_service: OrderDetailServ, currentUser: CurrentUser):
    result = await order_detail_service.get_details_by_order_id(order_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.get("/{order_detail_id}", response_model=OrderDetailOutSchema)
async def get_order_detail(order_detail_id: int, order_detail_service: OrderDetailServ, currentUser: CurrentUser):
    result = await order_detail_service.get_order_detail(order_detail_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.post("", response_model=OrderDetailOutSchema)
async def create_order_detail(order_detail_data: OrderDetailCreateSchema, order_detail_service: OrderDetailServ, currentUser: CurrentUser):
    result = await order_detail_service.create_order_detail(
        order_detail_data.OrderID, order_detail_data.ProductID, 
        order_detail_data.Quantity
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.put("/{order_detail_id}", response_model=OrderDetailOutSchema)
async def update_order_detail(order_detail_id: int, order_detail_data: OrderDetailCreateSchema, 
                             order_detail_service: OrderDetailServ, currentUser: CurrentUser):
    result = await order_detail_service.update_order_detail(
        order_detail_id, order_detail_data.OrderID, order_detail_data.ProductID,
        order_detail_data.Quantity
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.delete("/{order_detail_id}")
async def delete_order_detail(order_detail_id: int, order_detail_service: OrderDetailServ, currentUser: CurrentUser):
    order_detail = await order_detail_service.get_order_detail(order_detail_id)
    if not order_detail:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    delete_result = await order_detail_service.delete_order_detail(order_detail_id)
    if not delete_result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return {"message": f"Order detail {order_detail.OrderDetailID} has been deleted"}