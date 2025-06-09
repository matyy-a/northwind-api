from app.repository.employee_repository import EmployeeRepository
from app.models.sales.employee_model import Employee
from datetime import date

class EmployeeService:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository
    
    async def get_all_employees(self) -> list[Employee]:
        return await self.employee_repository.get_all()

    async def get_employee(self, id_employee: int) -> Employee | None:
        return await self.employee_repository.get_employee(id_employee)
    
    async def update_employee(self, id_employee: int, last_name: str, first_name: str,
                            birth_date: date, photo: str, notes: str) -> Employee | None:
        return await self.employee_repository.update_employee(id_employee, last_name, first_name,
                                                            birth_date, photo, notes)
    
    async def delete_employee(self, id_employee: int) -> bool:
        return await self.employee_repository.delete_employee(id_employee)
    
    async def create_employee(self, last_name: str, first_name: str, birth_date: date,
                            photo: str, notes: str) -> Employee | None:
        return await self.employee_repository.create_employee(last_name, first_name, birth_date,
                                                            photo, notes)