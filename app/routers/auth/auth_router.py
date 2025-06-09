import secrets
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth.auth_schema import Token
from app.dependencies.dependencies import AuthServ, AuthGoogleServ, CurrentUser, TokenDep

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: AuthServ
) -> Token:
    user = await auth_service.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrecto",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = await auth_service.login(form_data.username, form_data.password)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error al generar token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return token

@router.get("/google/url")
async def login_with_google(auth_google_service: AuthGoogleServ):
    """URL de autorización de Google OAuth"""
    try:
        # PKCE
        code_verifier = auth_google_service.generate_code_verifier()
        code_challenge = auth_google_service.generate_code_challenge(code_verifier)

        # STATE
        state = secrets.token_urlsafe(16)

        # Almacenar state y verifier en Redis
        auth_google_service.store_state_verifier(state, code_verifier)

        # Generar URL de autorización
        auth_url = auth_google_service.generate_auth_url(state, code_challenge)

        return {"auth_url": auth_url}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al generar URL de Google OAuth"
        )

@router.get("/google/callback")
async def google_callback(
    code: str,
    state: str,
    auth_google_service: AuthGoogleServ
) -> Token:
    """Callback de Google OAuth que completa el flujo de autenticación"""
    try:
        token = await auth_google_service.complete_oauth_flow(code, state)
        return token
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor durante la autenticación con Google"
        )

@router.post("/logout")
async def logout(current_user: CurrentUser, token: TokenDep, auth_service: AuthServ):
    """Invalido Token al cerrar la sesión"""
    success = await auth_service.logout(token)
    
    if success:
        return {"message": "Sesión cerrada exitosamente"}
       
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Token no válido o ya expirado"
    )