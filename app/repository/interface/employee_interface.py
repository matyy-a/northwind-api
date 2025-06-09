from abc import ABC, abstractmethod
from app.models.sales.employee_model import Employee
from datetime import date

class EmployeeInterface:

    @abstractmethod
    async def get_employee(self, id: int) -> Employee | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[Employee]:
        pass

    @abstractmethod
    async def create_employee(self, last_name: str, first_name: str, birth_date: date,
                        photo: str, notes: str) -> Employee | None:
        pass

    @abstractmethod
    async def update_employee(self, employee_id: int, last_name: str, first_name: str,
                        birth_date: date, photo: str, notes: str) -> Employee | None:
        pass

    @abstractmethod
    async def delete_employee(self, employee_id: int) -> bool:
        pass