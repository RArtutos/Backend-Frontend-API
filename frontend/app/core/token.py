from typing import Optional, Dict
from jose import jwt, JWTError
import logging

class TokenService:
    @staticmethod
    def decode_token(token: str) -> Optional[Dict]:
        try:
            # Decode without verification since we trust our backend
            payload = jwt.decode(token, options={"verify_signature": False})
            logging.debug(f"Decoded token payload: {payload}")
            return payload
        except JWTError as e:
            logging.error(f"Error decoding token: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error decoding token: {str(e)}")
            return None

    @staticmethod
    def extract_user_info(token: str) -> Optional[Dict]:
        payload = TokenService.decode_token(token)
        if not payload:
            return None
            
        # The backend sets 'sub' as the email
        email = payload.get('sub')
        if not email:
            logging.error("Token payload missing 'sub' claim")
            return None

        return {
            'email': email,
            'is_admin': payload.get('is_admin', False)
        }