from app.repository.interface.employee_interface import EmployeeInterface
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from app.models.sales.employee_model import Employee
from datetime import date

class EmployeeRepository(EmployeeInterface):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_employee(self, id: int) -> Employee | None:
        result = await self.db_session.execute(
            select(Employee).where(Employee.EmployeeID == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Employee]:
        result = await self.db_session.execute(select(Employee))
        return result.scalars().all()

    async def create_employee(self, last_name: str, first_name: str, birth_date: date,
                            photo: str, notes: str) -> Employee | None:
        new_employee = Employee(
            LastName=last_name,
            FirstName=first_name,
            BirthDate=birth_date,
            Photo=photo,
            Notes=notes
        )
        try:
            self.db_session.add(new_employee)
            await self.db_session.commit()
            await self.db_session.refresh(new_employee)
            return new_employee
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def update_employee(self, employee_id: int, last_name: str, first_name: str,
                            birth_date: date, photo: str, notes: str) -> Employee | None:
        result = await self.db_session.execute(
            select(Employee).where(Employee.EmployeeID == employee_id)
        )
        employee = result.scalar_one_or_none()

        if not employee:
            return None

        employee.LastName = last_name
        employee.FirstName = first_name
        employee.BirthDate = birth_date
        employee.Photo = photo
        employee.Notes = notes

        try:
            await self.db_session.commit()
            await self.db_session.refresh(employee)
            return employee
        except IntegrityError:
            await self.db_session.rollback()
            return None
        
    async def delete_employee(self, employee_id: int) -> bool:
        result = await self.db_session.execute(
            select(Employee).where(Employee.EmployeeID == employee_id)
        )
        employee = result.scalar_one_or_none()

        if not employee:
            return False

        try:
            await self.db_session.delete(employee)
            await self.db_session.commit()
            return True
        except Exception:
            await self.db_session.rollback()
            return False