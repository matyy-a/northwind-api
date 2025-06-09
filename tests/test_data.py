import pytest
from unittest.mock import Mock
from proyecto1.app.models.auth.user_model import User

mock_settings = Mock()
mock_settings.secret_key = "test_secret_key"
mock_settings.algorithm = "HS256"
mock_settings.access_token_expire_minutes = 30
mock_settings.google_client_id = "test_client_id"
mock_settings.google_client_secret = "test_client_secret"
mock_settings.google_redirect_uri = "http://localhost:8000/auth/google/callback"
mock_settings.google_auth_url = "https://accounts.google.com/o/oauth2/auth"
mock_settings.google_token_url = "https://oauth2.googleapis.com/token"
mock_settings.google_user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
mock_settings.redis_host = "localhost"
mock_settings.redis_port = 6379

test_user_input = {
    "username": "testuser",
    "email": "test@test.com",
    "password": "password_123"
}

hashed_password = "hashed_password_123"

test_user_db = User(
    id=1,
    username=test_user_input["username"],
    email=test_user_input["email"],
    hashed_password=hashed_password
)

@pytest.fixture
def test_config_token():
    return {
        "secret_key": "clave_secreta",
        "algorithm": "HS256",
        "expire_minutes": 15,
    }