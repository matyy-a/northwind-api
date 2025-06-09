from fastapi import APIRouter, HTTPException, status
from typing import List
from app.dependencies.dependencies import EmployeeServ, CurrentUser
from app.schemas.sales.employee_schema import EmployeeOutSchema, EmployeeCreateSchema

router = APIRouter(prefix="/employee", tags=["employee"])

@router.get("/all", response_model=List[EmployeeOutSchema])
async def get_all_employees(employee_service: EmployeeServ, currentUser: CurrentUser):
    return await employee_service.get_all_employees()

@router.get("/{id_employee}", response_model=EmployeeOutSchema)
async def get_employee(id_employee: int, employee_service: EmployeeServ, currentUser: CurrentUser):
    result = await employee_service.get_employee(id_employee)
    if not result:         
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return result

@router.post("", response_model=EmployeeOutSchema)
async def create_employee(employee_data: EmployeeCreateSchema, employee_service: EmployeeServ, currentUser: CurrentUser):
    return await employee_service.create_employee(
        employee_data.LastName, employee_data.FirstName, employee_data.BirthDate,
        employee_data.Photo, employee_data.Notes
    )

@router.put("/{id_employee}", response_model=EmployeeOutSchema)
async def update_employee(id_employee: int, employee_data: EmployeeCreateSchema, employee_service: EmployeeServ, currentUser: CurrentUser):
    result = await employee_service.update_employee(
        id_employee, employee_data.LastName, employee_data.FirstName, employee_data.BirthDate,
        employee_data.Photo, employee_data.Notes
    )
    if not result:         
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return result

@router.delete("/{id_employee}")
async def delete_employee(id_employee: int, employee_service: EmployeeServ, currentUser: CurrentUser):
    result = await employee_service.get_employee(id_employee)
    delete = await employee_service.delete_employee(id_employee)
    if not delete:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return {"message": f"employee {result.FirstName} {result.LastName} has been deleted"}