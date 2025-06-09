import pytest
from fastapi import HTTPException
from datetime import timedelta
from unittest.mock import AsyncMock, Mock, patch
from tests.test_data import mock_settings

with patch.dict('sys.modules', {'app.utils.config': Mock(settings=mock_settings)}):
    from app.services.auth.auth_service import AuthService
    from app.schemas.auth.auth_schema import Token
    from tests.test_data import test_user_db, test_user_input

class TestAuthService:
    @pytest.fixture
    def mock_user_repository(self):
        return AsyncMock()
    
    @pytest.fixture
    def mock_security_service(self):
        return Mock()
    
    @pytest.fixture
    def mock_token_service(self):
        return AsyncMock()
    
    @pytest.fixture
    def auth_service(self, mock_user_repository, mock_security_service, mock_token_service):
        return AuthService(mock_user_repository, mock_security_service, mock_token_service)
    
    @pytest.mark.asyncio
    async def test_authenticate_success(self, auth_service, mock_user_repository, mock_security_service):
        # Arrange
        mock_user_repository.get_user_by_username_or_email.return_value = test_user_db
        mock_security_service.verify_password.return_value = True

        # Act
        result = await auth_service.authenticate(test_user_input["username"], test_user_input["password"])

        # Assert
        assert result == test_user_db
        mock_user_repository.get_user_by_username_or_email.assert_called_once_with(test_user_input["username"])
        mock_security_service.verify_password.assert_called_once_with(test_user_input["password"], test_user_db.hashed_password)

    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(self, auth_service, mock_user_repository, mock_security_service):
        # Arrange
        mock_user_repository.get_user_by_username_or_email.return_value = None

        # Act
        result = await auth_service.authenticate(test_user_input["username"], test_user_input["password"])

        # Assert
        assert result is False
        mock_user_repository.get_user_by_username_or_email.assert_called_once_with(test_user_input["username"])
        mock_security_service.verify_password.assert_not_called()

    @pytest.mark.asyncio
    async def test_authenticate_wrong_password(self, auth_service, mock_user_repository, mock_security_service):
        # Arrange
        mock_user_repository.get_user_by_username_or_email.return_value = test_user_db
        mock_security_service.verify_password.return_value = False

        # Act
        result = await auth_service.authenticate(test_user_input["username"], "wrong_password")

        # Assert
        assert result is False
        mock_user_repository.get_user_by_username_or_email.assert_called_once_with(test_user_input["username"])
        mock_security_service.verify_password.assert_called_once_with("wrong_password", test_user_db.hashed_password)

    @pytest.mark.asyncio
    async def test_login_success(self, auth_service, mock_user_repository, mock_security_service, mock_token_service):
        # Arrange
        mock_user_repository.get_user_by_username_or_email.return_value = test_user_db
        mock_security_service.verify_password.return_value = True
        mock_token_service.create_access_token.return_value = "test_token"

        # Act
        result = await auth_service.login(test_user_input["username"], test_user_input["password"])

        # Assert
        assert isinstance(result, Token)
        assert result.access_token == "test_token"
        assert result.token_type == "bearer"
        mock_token_service.create_access_token.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_failure(self, auth_service, mock_user_repository, mock_security_service, mock_token_service):
        # Arrange
        mock_user_repository.get_user_by_username_or_email.return_value = None

        # Act
        result = await auth_service.login(test_user_input["username"], test_user_input["password"])

        # Assert
        assert result is None
        mock_token_service.create_access_token.assert_not_called()

    @pytest.mark.asyncio
    async def test_logout_success(self, auth_service, mock_token_service):
        # Arrange
        test_token = "test_token"
        mock_token_service.invalidate_token.return_value = True

        # Act
        result = await auth_service.logout(test_token)

        # Assert
        assert result is True
        mock_token_service.invalidate_token.assert_called_once_with(test_token)

    @pytest.mark.asyncio
    async def test_get_current_user_from_token_success(self, auth_service, mock_user_repository, mock_token_service):
        # Arrange
        test_token = "test_token"
        payload = {"sub": test_user_input["username"]}
        mock_token_service.decode_access_token.return_value = payload
        mock_user_repository.get_user_by_username_or_email.return_value = test_user_db

        # Act
        result = await auth_service.get_current_user_from_token(test_token)

        # Assert
        assert result == test_user_db
        mock_token_service.decode_access_token.assert_called_once_with(test_token)
        mock_user_repository.get_user_by_username_or_email.assert_called_once_with(test_user_input["username"])

    @pytest.mark.asyncio
    async def test_get_current_user_from_token_no_username(self, auth_service, mock_user_repository, mock_token_service):
        # Arrange
        test_token = "test_token"
        payload = {"sub": None}
        mock_token_service.decode_access_token.return_value = payload

        # Act
        result = await auth_service.get_current_user_from_token(test_token)

        # Assert
        assert result is None
        mock_token_service.decode_access_token.assert_called_once_with(test_token)
        mock_user_repository.get_user_by_username_or_email.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_current_user_from_token_invalid_token(self, auth_service, mock_user_repository, mock_token_service):
        # Arrange
        test_token = "invalid_token"
        mock_token_service.decode_access_token.side_effect = HTTPException(status_code=401, detail="Invalid token")

        # Act
        result = await auth_service.get_current_user_from_token(test_token)

        # Assert
        assert result is None
        mock_token_service.decode_access_token.assert_called_once_with(test_token)
        mock_user_repository.get_user_by_username_or_email.assert_not_called()