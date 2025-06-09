import pytest
from fastapi import HTTPException
from datetime import timedelta
from unittest.mock import AsyncMock, Mock
from app.services.auth.token_service import TokenService
from tests.test_data import test_config_token, test_user_input

class TestTokenService:
    @pytest.fixture
    def mock_blacklist_service(self):
        return Mock()
    
    @pytest.fixture
    def token_service(self, test_config_token, mock_blacklist_service):
        return TokenService(**test_config_token, blacklist_service=mock_blacklist_service)
    
    @pytest.mark.asyncio
    async def test_process_token_success(self, token_service, mock_blacklist_service):
        # Arrange
        data = {"sub": test_user_input["username"]}
        expire_delta = timedelta(minutes=token_service.expire_minutes)
        mock_blacklist_service.is_token_blacklist.return_value = False

        # Act
        token_encoded = await token_service.create_access_token(
            data=data, expire_delta=expire_delta
        )

        result = await token_service.decode_access_token(token_encoded)

        # Assert
        assert result["sub"] == test_user_input["username"]
        assert "exp" in result
        assert "jti" in result

    @pytest.mark.asyncio
    async def test_process_token_invalid(self, token_service, mock_blacklist_service):
        # Arrange
        data = {"sub": test_user_input["username"]}
        expire_delta = timedelta(minutes=token_service.expire_minutes)
        mock_blacklist_service.is_token_blacklist.return_value = True

        # Act
        token_encoded = await token_service.create_access_token(
            data=data, expire_delta=expire_delta
        )

        with pytest.raises(HTTPException) as exc_info:
            await token_service.decode_access_token(token_encoded)

        # Assert
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Token inválido"

    @pytest.mark.asyncio
    async def test_invalidate_token_success(self, token_service, mock_blacklist_service):
        # Arrange
        data = {"sub": test_user_input["username"]}
        expire_delta = timedelta(minutes=token_service.expire_minutes)
        mock_blacklist_service.is_token_blacklist.return_value = False
        token = await token_service.create_access_token(data=data, expire_delta=expire_delta)

        # Act
        result = await token_service.invalidate_token(token)

        # Assert
        assert result is True
        decode = await token_service.decode_access_token(token)
        mock_blacklist_service.blacklist_token.assert_called_with(decode["jti"], decode["exp"])

    @pytest.mark.asyncio
    async def test_invalidate_token_invalid(self, token_service, mock_blacklist_service):
        # Arrange
        data = {"sub": test_user_input["username"]}
        expire_delta = timedelta(minutes=token_service.expire_minutes)
        mock_blacklist_service.is_token_blacklist.return_value = True
        token = await token_service.create_access_token(data=data)

        # Act
        result = await token_service.invalidate_token(token)

        # Assert
        assert result is False
        mock_blacklist_service.blacklist_token.assert_not_called()

