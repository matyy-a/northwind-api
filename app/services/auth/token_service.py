import uuid
from jose import jwt, JWTError
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from app.services.auth.token_blacklist_service import TokenBlackListService

class TokenService:
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int, blacklist_service: TokenBlackListService):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes
        self.blacklist = blacklist_service

    async def create_access_token(self, data: dict, expire_delta: timedelta | None = None):
        to_encode = data.copy()
        if expire_delta:
            expire = datetime.now(timezone.utc) + expire_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        to_encode.update({
            "exp": expire,
            "jti": str(uuid.uuid4())
        })

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    async def decode_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            jti = payload.get("jti")

            if jti and self.blacklist.is_token_blacklist(jti):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido"
                )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
    async def invalidate_token(self, token: str) -> bool:
        try:
            payload = await self.decode_access_token(token)
            jti = payload.get("jti")
            exp = payload.get("exp")

            if jti and exp:
                self.blacklist.blacklist_token(jti, exp)
                return True
            return False
        except HTTPException:
            return False