import pytest
from unittest.mock import AsyncMock, Mock, patch
from tests.test_data import mock_settings

with patch.dict('sys.modules', {'app.utils.config': Mock(settings=mock_settings)}):
    from app.services.auth.auth_google_service import AuthGoogleService
    from app.schemas.auth.auth_schema import Token
    from tests.test_data import test_user_db

class TestAuthGoogleService:
    @pytest.fixture
    def mock_redis_client(self):
        return Mock()
    
    @pytest.fixture
    def mock_auth_service(self):
        return AsyncMock()
    
    @pytest.fixture
    def mock_user_service(self):
        return AsyncMock()
    
    @pytest.fixture
    def mock_token_service(self):
        return AsyncMock()
    
    @pytest.fixture
    def auth_google_service(self, mock_redis_client, mock_auth_service, mock_user_service, mock_token_service):
        return AuthGoogleService(mock_redis_client, mock_auth_service, mock_user_service, mock_token_service)
    
    @pytest.mark.asyncio
    async def test_login_existing_user(self, auth_google_service, mock_user_service, mock_token_service):
        # Arrange
        user_info = {"email": "test@example.com"}
        mock_user_service.get_user.return_value = test_user_db
        mock_token_service.create_access_token.return_value = "test_token"

        # Act
        result = await auth_google_service.login(user_info)

        # Assert
        assert isinstance(result, Token)
        assert result.access_token == "test_token"
        assert result.token_type == "bearer"
        mock_user_service.get_user.assert_called_once_with("test@example.com")
        mock_user_service.create_user.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_new_user(self, auth_google_service, mock_user_service, mock_token_service):
        # Arrange
        user_info = {"email": "newuser@example.com"}
        mock_user_service.get_user.return_value = None
        mock_user_service.create_user.return_value = test_user_db
        mock_token_service.create_access_token.return_value = "test_token"

        # Act
        result = await auth_google_service.login(user_info)

        # Assert
        assert isinstance(result, Token)
        assert result.access_token == "test_token"
        assert result.token_type == "bearer"
        mock_user_service.get_user.assert_called_once_with("newuser@example.com")
        mock_user_service.create_user.assert_called_once_with("newuser", "newuser@example.com", "newuser@example.com")

    def test_generate_code_verifier(self, auth_google_service):
        # Act
        verifier = auth_google_service.generate_code_verifier()

        # Assert
        assert isinstance(verifier, str)
        assert len(verifier) > 0

    def test_generate_code_challenge(self, auth_google_service):
        # Arrange
        verifier = "test_verifier"

        # Act
        challenge = auth_google_service.generate_code_challenge(verifier)

        # Assert
        assert isinstance(challenge, str)
        assert len(challenge) > 0
        assert challenge != verifier 

    def test_store_state_verifier(self, auth_google_service, mock_redis_client):
        # Arrange
        state = "test_state"
        verifier = "test_verifier"

        # Act
        auth_google_service.store_state_verifier(state, verifier)

        # Assert
        mock_redis_client.setex.assert_called_once_with(f"oauth_state:{state}", 300, verifier)

    def test_get_and_delete_verifier_success(self, auth_google_service, mock_redis_client):
        # Arrange
        state = "test_state"
        mock_redis_client.get.return_value = b"test_verifier"

        # Act
        result = auth_google_service.get_and_delete_verifier(state)

        # Assert
        assert result == "test_verifier"
        mock_redis_client.get.assert_called_once_with(f"oauth_state:{state}")
        mock_redis_client.delete.assert_called_once_with(f"oauth_state:{state}")

    def test_get_and_delete_verifier_not_found(self, auth_google_service, mock_redis_client):
        # Arrange
        state = "test_state"
        mock_redis_client.get.return_value = None

        # Act
        result = auth_google_service.get_and_delete_verifier(state)

        # Assert
        assert result is None
        mock_redis_client.get.assert_called_once_with(f"oauth_state:{state}")
        mock_redis_client.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_complete_oauth_flow_success(self, auth_google_service, mock_redis_client, mock_user_service, mock_token_service):
        # Arrange
        code = "test_code"
        state = "test_state"
        mock_redis_client.get.return_value = b"test_verifier"
        mock_user_service.get_user.return_value = test_user_db
        mock_token_service.create_access_token.return_value = "test_token"
        
        with patch.object(auth_google_service, 'exchange_code_for_token', return_value="google_token"), \
             patch.object(auth_google_service, 'get_user_info', return_value={"email": "test@example.com"}):

            # Act
            result = await auth_google_service.complete_oauth_flow(code, state)

            # Assert
            assert isinstance(result, Token)
            assert result.access_token == "test_token"
            assert result.token_type == "bearer"

    @pytest.mark.asyncio
    async def test_complete_oauth_flow_invalid_state(self, auth_google_service, mock_redis_client):
        # Arrange
        code = "test_code"
        state = "invalid_state"
        mock_redis_client.get.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Estado inválido o expirado"):
            await auth_google_service.complete_oauth_flow(code, state)

    @pytest.mark.asyncio
    async def test_complete_oauth_flow_no_google_token(self, auth_google_service, mock_redis_client):
        # Arrange
        code = "test_code"
        state = "test_state"
        mock_redis_client.get.return_value = b"test_verifier"
        
        with patch.object(auth_google_service, 'exchange_code_for_token', return_value=None):
            # Act & Assert
            with pytest.raises(ValueError, match="No se pudo obtener el token de Google"):
                await auth_google_service.complete_oauth_flow(code, state)

    @pytest.mark.asyncio
    async def test_complete_oauth_flow_no_user_info(self, auth_google_service, mock_redis_client):
        # Arrange
        code = "test_code"
        state = "test_state"
        mock_redis_client.get.return_value = b"test_verifier"
        
        with patch.object(auth_google_service, 'exchange_code_for_token', return_value="google_token"), \
             patch.object(auth_google_service, 'get_user_info', return_value=None):

            # Act & Assert
            with pytest.raises(ValueError, match="No se pudo obtener información del usuario de Google"):
                await auth_google_service.complete_oauth_flow(code, state)