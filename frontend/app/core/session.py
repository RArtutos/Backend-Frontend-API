"""Session management module"""
from flask import session
from typing import Optional, Dict

class SessionManager:
    @staticmethod
    def set_user_session(user_data: Dict) -> None:
        """Set user session data"""
        session['user_token'] = user_data['token']
        session['user_email'] = user_data['email']
        session['is_admin'] = user_data['is_admin']
        session.permanent = True

    @staticmethod
    def clear_session() -> None:
        """Clear all session data"""
        session.clear()

    @staticmethod
    def get_stored_token() -> Optional[str]:
        """Get stored authentication token"""
        return session.get('user_token')

    @staticmethod
    def get_user_data() -> Optional[Dict]:
        """Get all user session data"""
        if 'user_token' not in session:
            return None
        return {
            'token': session['user_token'],
            'email': session['user_email'],
            'is_admin': session['is_admin']
        }