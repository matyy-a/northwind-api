import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
from app.services.auth.token_blacklist_service import TokenBlackListService

class TestTokenBlackListService:
    @pytest.fixture
    def mock_redis_client(self):
        return Mock()
    
    @pytest.fixture
    def blacklist_service(self, mock_redis_client):
        return TokenBlackListService(mock_redis_client)
    
    @patch('app.services.token_blacklist_service.datetime')
    def test_blacklist_token_success(self, mock_datetime, blacklist_service, mock_redis_client):
        # Arrange
        jti = "test_jti"
        exp = 1700000000 
        current_timestamp = 1699999000  
        expected_ttl = exp - current_timestamp  
        
        mock_now = Mock()
        mock_now.timestamp.return_value = current_timestamp
        mock_datetime.now.return_value = mock_now
        mock_datetime.timezone = timezone
        
        # Act
        blacklist_service.blacklist_token(jti, exp)
        
        # Assert
        mock_redis_client.setex.assert_called_once_with(f"blacklist:{jti}", expected_ttl, "true")
        mock_datetime.now.assert_called_once_with(timezone.utc)

    @patch('app.services.token_blacklist_service.datetime')
    def test_blacklist_token_expired(self, mock_datetime, blacklist_service, mock_redis_client):
        # Arrange
        jti = "test_jti"
        exp = 1699999000  
        current_timestamp = 1700000000  
        
        mock_now = Mock()
        mock_now.timestamp.return_value = current_timestamp
        mock_datetime.now.return_value = mock_now
        mock_datetime.timezone = timezone
        
        # Act
        blacklist_service.blacklist_token(jti, exp)
        
        # Assert
        mock_redis_client.setex.assert_called_once_with(f"blacklist:{jti}", 0, "true")

    def test_is_token_blacklist_true(self, blacklist_service, mock_redis_client):
        # Arrange
        jti = "test_jti"
        mock_redis_client.exists.return_value = 1
        
        # Act
        result = blacklist_service.is_token_blacklist(jti)
        
        # Assert
        assert result is True
        mock_redis_client.exists.assert_called_once_with(f"blacklist:{jti}")

    def test_is_token_blacklist_false(self, blacklist_service, mock_redis_client):
        # Arrange
        jti = "test_jti"
        mock_redis_client.exists.return_value = 0
        
        # Act
        result = blacklist_service.is_token_blacklist(jti)
        
        # Assert
        assert result is False
        mock_redis_client.exists.assert_called_once_with(f"blacklist:{jti}")

    def test_is_token_blacklist_multiple_tokens(self, blacklist_service, mock_redis_client):
        # Arrange
        jti1 = "test_jti_1"
        jti2 = "test_jti_2"
        mock_redis_client.exists.side_effect = [1, 0] 
        
        # Act
        result1 = blacklist_service.is_token_blacklist(jti1)
        result2 = blacklist_service.is_token_blacklist(jti2)
        
        # Assert
        assert result1 is True
        assert result2 is False
        assert mock_redis_client.exists.call_count == 2

    @patch('app.services.token_blacklist_service.datetime')
    def test_blacklist_token_with_zero_ttl(self, mock_datetime, blacklist_service, mock_redis_client):
        # Arrange
        jti = "test_jti"
        exp = 1700000000
        current_timestamp = 1700000000 
        
        mock_now = Mock()
        mock_now.timestamp.return_value = current_timestamp
        mock_datetime.now.return_value = mock_now
        mock_datetime.timezone = timezone
        
        # Act
        blacklist_service.blacklist_token(jti, exp)
        
        # Assert
        mock_redis_client.setex.assert_called_once_with(f"blacklist:{jti}", 0, "true")

    @patch('app.services.token_blacklist_service.datetime')
    def test_blacklist_token_with_negative_ttl(self, mock_datetime, blacklist_service, mock_redis_client):
        # Arrange
        jti = "test_jti"
        exp = 1699999000 
        current_timestamp = 1700001000  
        
        mock_now = Mock()
        mock_now.timestamp.return_value = current_timestamp
        mock_datetime.now.return_value = mock_now
        mock_datetime.timezone = timezone
        
        # Act
        blacklist_service.blacklist_token(jti, exp)
        
        # Assert
        mock_redis_client.setex.assert_called_once_with(f"blacklist:{jti}", 0, "true")

    def test_initialization(self, mock_redis_client):
        # Act
        service = TokenBlackListService(mock_redis_client)
        
        # Assert
        assert service.redis_client == mock_redis_client

    def test_blacklist_token_key_format(self, blacklist_service, mock_redis_client):
        # Arrange
        jti = "unique_token_id_123"
        exp = 1700000000
        
        with patch('app.services.token_blacklist_service.datetime') as mock_datetime:
            mock_now = Mock()
            mock_now.timestamp.return_value = 1699999000
            mock_datetime.now.return_value = mock_now
            mock_datetime.timezone = timezone
            
            # Act
            blacklist_service.blacklist_token(jti, exp)
            
            # Assert
            expected_key = f"blacklist:{jti}"
            mock_redis_client.setex.assert_called_once()
            call_args = mock_redis_client.setex.call_args[0]
            assert call_args[0] == expected_key

    def test_is_token_blacklist_key_format(self, blacklist_service, mock_redis_client):
        # Arrange
        jti = "unique_token_id_456"
        mock_redis_client.exists.return_value = 1
        
        # Act
        blacklist_service.is_token_blacklist(jti)
        
        # Assert
        expected_key = f"blacklist:{jti}"
        mock_redis_client.exists.assert_called_once_with(expected_key)