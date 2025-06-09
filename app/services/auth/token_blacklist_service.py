from redis import Redis
from datetime import datetime, timezone

class TokenBlackListService:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def blacklist_token(self, jti: str, exp: int):
        current_time = datetime.now(timezone.utc).timestamp()
        ttl = max(0, int(exp - current_time))
        self.redis_client.setex(f"blacklist:{jti}", ttl, "true")

    def is_token_blacklist(self, jti: str) -> bool:
        return self.redis_client.exists(f"blacklist:{jti}") == 1