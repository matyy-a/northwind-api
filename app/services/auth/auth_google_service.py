import secrets
import hashlib
import base64
import httpx
from redis import Redis
from datetime import timedelta
from app.utils.config import settings
from app.services.auth.auth_service import AuthService
from app.services.auth.user_service import UserService
from app.services.auth.token_service import TokenService
from app.schemas.auth.auth_schema import Token
from app.utils.config import settings

class AuthGoogleService:
    def __init__(self, redis_client: Redis, auth_service: AuthService, user_service: UserService, token_service: TokenService):
        self.redis = redis_client
        self.auth_service = auth_service
        self.user_service = user_service
        self.token_service = token_service

    async def login(self, user_info: dict) -> Token:
        email = user_info.get("email")
        user = await self.user_service.get_user(email)

        if not user:
            username = email.split("@")[0]
            user = await self.user_service.create_user(username, email, email)
        
        access_token = await self.token_service.create_access_token(
            data={"sub": user.username}, expire_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )

        return Token(access_token=access_token, token_type="bearer")

    def generate_code_verifier(self):
        return secrets.token_urlsafe(64)
    
    def generate_code_challenge(self, verifier):
        sha256 = hashlib.sha256(verifier.encode()).digest()
        return base64.urlsafe_b64encode(sha256).decode().rstrip("=")
    
    def generate_auth_url(self, state: str, code_challenge: str) -> str:
        return (
            f"{settings.google_auth_url}"
            f"?client_id={settings.google_client_id}"
            f"&redirect_uri={settings.google_redirect_uri}"
            "&scope=openid email profile"
            "&response_type=code"
            "&access_type=offline"
            "&prompt=consent"
            f"&state={state}"
            f"&code_challenge={code_challenge}"
            "&code_challenge_method=S256"
        )
    
    def store_state_verifier(self, state: str, verifier: str):
        self.redis.setex(f"oauth_state:{state}", 300, verifier)

    def get_and_delete_verifier(self, state: str) -> str | None:
        verifier = self.redis.get(f"oauth_state:{state}")
        if verifier:
            self.redis.delete(f"oauth_state:{state}")
        return verifier.decode() if isinstance(verifier, bytes) else verifier
    
    async def exchange_code_for_token(self, code: str, code_verifier: str) -> str:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                settings.google_token_url,
                data={
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "code": code,
                    "code_verifier": code_verifier,
                    "grant_type": "authorization_code",
                    "redirect_uri": settings.google_redirect_uri,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        return token_response.json().get("access_token")

    async def get_user_info(self, access_token: str) -> dict:
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                settings.google_user_info_url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
        return user_response.json()
    
    async def complete_oauth_flow(self, code: str, state: str) -> Token:
        """
        Completa el flujo OAuth de Google y devuelve un token de acceso
        """
        # Verificar state y obtener code_verifier
        code_verifier = self.get_and_delete_verifier(state)
        if not code_verifier:
            raise ValueError("Estado inválido o expirado")
        
        # Intercambiar código por token de Google
        google_access_token = await self.exchange_code_for_token(code, code_verifier)
        if not google_access_token:
            raise ValueError("No se pudo obtener el token de Google")
        
        # Obtener información del usuario
        user_info = await self.get_user_info(google_access_token)
        if not user_info:
            raise ValueError("No se pudo obtener información del usuario de Google")
        
        # Autenticar/crear usuario y generar token
        return await self.login(user_info)