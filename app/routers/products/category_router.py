from fastapi import APIRouter, HTTPException, status
from typing import List
from app.dependencies.dependencies import CategoryServ, CurrentUser
from app.schemas.products.category_schema import CategoryOutSchema, CategoryCreateSchema

router = APIRouter(prefix="/category", tags=["category"])

@router.get("/all", response_model=List[CategoryOutSchema])
async def get_all_categories(category_service: CategoryServ, currentUser: CurrentUser):
    return await category_service.get_all_categories()

@router.get("/{id_category}", response_model=CategoryOutSchema)
async def get_category(id_category: int, category_service: CategoryServ, currentUser: CurrentUser):
    result = await category_service.get_category(id_category)
    if not result:         
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.post("", response_model=CategoryOutSchema)
async def create_category(category_data: CategoryCreateSchema, category_service: CategoryServ, currentUser: CurrentUser):
    return await category_service.create_category(category_data.CategoryName, category_data.Description)

@router.put("/{id_category}", response_model=CategoryOutSchema)
async def update_category(id_category: int, category_data: CategoryCreateSchema, category_service: CategoryServ, currentUser: CurrentUser):
    result = await category_service.update_category(id_category, category_data.CategoryName, category_data.Description)
    if not result:         
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return result

@router.delete("/{id_category}")
async def delete_category(id_category: int, category_service: CategoryServ, currentUser: CurrentUser):
    result = await category_service.get_category(id_category)
    delete = await category_service.delete_category(id_category)
    if not delete:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return {"message": f"category {result.CategoryName} has been deleted"}
