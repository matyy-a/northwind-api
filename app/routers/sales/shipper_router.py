from fastapi import APIRouter, HTTPException, status
from typing import List
from app.dependencies.dependencies import ShipperServ, CurrentUser
from app.schemas.sales.shipper_schema import ShipperOutSchema, ShipperCreateSchema

router = APIRouter(prefix="/shipper", tags=["shipper"])

@router.get("/all", response_model=List[ShipperOutSchema])
async def get_all_shippers(shipper_service: ShipperServ, currentUser: CurrentUser):
    return await shipper_service.get_all_shippers()

@router.get("/{id_shipper}", response_model=ShipperOutSchema)
async def get_shipper(id_shipper: int, shipper_service: ShipperServ, currentUser: CurrentUser):
    result = await shipper_service.get_shipper(id_shipper)
    if not result:         
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return result

@router.post("", response_model=ShipperOutSchema)
async def create_shipper(shipper_data: ShipperCreateSchema, shipper_service: ShipperServ, currentUser: CurrentUser):
    return await shipper_service.create_shipper(shipper_data.ShipperName, shipper_data.Phone)

@router.put("/{id_shipper}", response_model=ShipperOutSchema)
async def update_shipper(id_shipper: int, shipper_data: ShipperCreateSchema, shipper_service: ShipperServ, currentUser: CurrentUser):
    result = await shipper_service.update_shipper(id_shipper, shipper_data.ShipperName, shipper_data.Phone)
    if not result:         
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return result

@router.delete("/{id_shipper}")
async def delete_shipper(id_shipper: int, shipper_service: ShipperServ, currentUser: CurrentUser):
    result = await shipper_service.get_shipper(id_shipper)
    delete = await shipper_service.delete_shipper(id_shipper)
    if not delete:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return {"message": f"shipper {result.ShipperName} has been deleted"}
