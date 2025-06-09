import pytest
from unittest.mock import AsyncMock, Mock
from app.services.auth.user_service import UserService
from tests.test_data import test_user_db, test_user_input, hashed_password

class TestUserService:
    @pytest.fixture
    def mock_user_repository(self):
        return AsyncMock()
    
    @pytest.fixture
    def mock_security_service(self):
        mock = Mock()
        mock.hash_password.return_value = hashed_password
        return mock
    
    @pytest.fixture
    def user_service(self, mock_user_repository, mock_security_service):
        return UserService(mock_user_repository, mock_security_service)
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, user_service, mock_user_repository, mock_security_service):
        # Arrange
        mock_user_repository.create_user.return_value = test_user_db

        # Act
        result = await user_service.create_user(**test_user_input)

        # Assert
        assert result == test_user_db
        mock_security_service.hash_password.assert_called_once_with(test_user_input["password"])
        mock_user_repository.create_user.assert_called_once_with(test_user_input["username"], test_user_input["email"], hashed_password)

    @pytest.mark.asyncio
    async def test_create_user_none(self, user_service, mock_user_repository, mock_security_service):
        # Arrange
        mock_user_repository.create_user.return_value = None

        # Act
        result = await user_service.create_user(**test_user_input)

        # Assert
        assert result is None
        mock_security_service.hash_password.assert_called_once_with(test_user_input["password"])
        mock_user_repository.create_user.assert_called_once_with(test_user_input["username"], test_user_input["email"], hashed_password)

    @pytest.mark.asyncio
    async def test_get_user_success(self, user_service, mock_user_repository, mock_security_service):
        #Arrange
        mock_user_repository.get_user_by_username_or_email.return_value = test_user_db

        # Act
        result = await user_service.get_user(test_user_input["username"])

        # Assert
        assert result == test_user_db
        mock_user_repository.get_user_by_username_or_email.assert_called_once_with(test_user_input["username"])
    
    @pytest.mark.asyncio
    async def test_get_user_none(self, user_service, mock_user_repository, mock_security_service):
        #Arrange
        mock_user_repository.get_user_by_username_or_email.return_value = None

        # Act
        result = await user_service.get_user(test_user_input["username"])

        # Assert
        assert result is None
        mock_user_repository.get_user_by_username_or_email.assert_called_once_with(test_user_input["username"])
