from fastapi import APIRouter, HTTPException, status
from app.schemas.auth.user_schema import UserCreateSchema
from app.dependencies.dependencies import UserServ

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/register")
async def register_new_user(new_user: UserCreateSchema, user_service: UserServ) -> dict[str, str]:
    try:
        user = await user_service.create_user(**new_user.model_dump())
        
        return {
            "message": "Usuario creado exitosamente",
            "user": user.username
        }       
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuario o Email ya registrado"
        )
