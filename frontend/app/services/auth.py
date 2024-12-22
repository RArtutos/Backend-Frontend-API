"""Authentication service module"""
import requests
from typing import Optional, Tuple
from ..models.user import User
from ..config import Config
from ..core.session import SessionManager

class AuthService:
    def __init__(self):
        self.api_url = f"{Config.API_URL}/api/auth"
    
    def login(self, email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """Authenticate user and create session"""
        try:
            response = requests.post(
                f"{self.api_url}/login",
                data={
                    'username': email,
                    'password': password
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            )
            
            if response.status_code != 200:
                return None, "Invalid credentials"
            
            data = response.json()
            if not data.get('access_token'):
                return None, "Invalid response from server"
                
            # Store the token in session
            SessionManager.set_user_session({
                'token': data['access_token'],
                'email': email,
                'is_admin': email == Config.ADMIN_EMAIL
            })
            
            # Create user object
            user = User(
                email=email,
                is_admin=True if email == Config.ADMIN_EMAIL else False
            )
            return user, None
            
        except requests.RequestException as e:
            return None, f"Connection error: {str(e)}"
        except Exception as e:
            return None, f"Login error: {str(e)}"

    def get_user(self, email: str) -> Optional[User]:
        """Get user by email"""
        if not email:
            return None
        return User(
            email=email,
            is_admin=True if email == Config.ADMIN_EMAIL else False
        )