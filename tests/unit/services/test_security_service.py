import pytest
from unittest.mock import Mock, patch
from app.services.auth.security_service import SecurityService


class TestSecurityService:
    @pytest.fixture
    def security_service(self):
        return SecurityService()
    
    def test_hash_password(self, security_service):
        # Arrange
        password = "test_password"
        
        # Act
        hashed = security_service.hash_password(password)
        
        # Assert
        assert isinstance(hashed, str)
        assert hashed != password  
        assert len(hashed) > 0
        assert hashed.startswith('$2b$')  

    def test_verify_password_correct(self, security_service):
        # Arrange
        password = "test_password"
        hashed = security_service.hash_password(password)
        
        # Act
        result = security_service.verify_password(password, hashed)
        
        # Assert
        assert result is True

    def test_verify_password_incorrect(self, security_service):
        # Arrange
        correct_password = "test_password"
        wrong_password = "wrong_password"
        hashed = security_service.hash_password(correct_password)
        
        # Act
        result = security_service.verify_password(wrong_password, hashed)
        
        # Assert
        assert result is False

    def test_verify_password_empty_password(self, security_service):
        # Arrange
        password = "test_password"
        hashed = security_service.hash_password(password)
        
        # Act
        result = security_service.verify_password("", hashed)
        
        # Assert
        assert result is False

    def test_hash_password_empty_string(self, security_service):
        # Arrange
        password = ""
        
        # Act
        hashed = security_service.hash_password(password)
        
        # Assert
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed.startswith('$2b$')

    def test_hash_password_same_input_different_output(self, security_service):
        # Arrange
        password = "test_password"
        
        # Act
        hash1 = security_service.hash_password(password)
        hash2 = security_service.hash_password(password)
        
        # Assert
        assert hash1 != hash2  
        assert security_service.verify_password(password, hash1)
        assert security_service.verify_password(password, hash2)

    @patch('app.services.security_service.CryptContext')
    def test_security_service_initialization(self, mock_crypt_context):
        # Arrange
        mock_context = Mock()
        mock_crypt_context.return_value = mock_context
        
        # Act
        service = SecurityService()
        
        # Assert
        mock_crypt_context.assert_called_once_with(schemes=["bcrypt"], deprecated="auto")
        assert service.pwd_context == mock_context

    def test_verify_password_with_mock_context(self):
        # Arrange
        with patch('app.services.security_service.CryptContext') as mock_crypt_context:
            mock_context = Mock()
            mock_context.verify.return_value = True
            mock_crypt_context.return_value = mock_context
            
            service = SecurityService()
            
            # Act
            result = service.verify_password("password", "hashed_password")
            
            # Assert
            assert result is True
            mock_context.verify.assert_called_once_with("password", "hashed_password")

    def test_hash_password_with_mock_context(self):
        # Arrange
        with patch('app.services.security_service.CryptContext') as mock_crypt_context:
            mock_context = Mock()
            mock_context.hash.return_value = "mocked_hash"
            mock_crypt_context.return_value = mock_context
            
            service = SecurityService()
            
            # Act
            result = service.hash_password("password")
            
            # Assert
            assert result == "mocked_hash"
            mock_context.hash.assert_called_once_with("password")