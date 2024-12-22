"""Utility functions for session management"""
from typing import Dict, Optional
from flask import session
from ..models.user import User

def get_user_from_session() -> Optional[User]:
    """Get user object from session data"""
    if 'user_email' not in session:
        return None
    return User(
        email=session['user_email'],
        is_admin=session.get('is_admin', False)
    )

def set_session_data(user_data: Dict) -> None:
    """Set user data in session"""
    session['user_email'] = user_data['email']
    session['is_admin'] = user_data.get('is_admin', False)
    session['token'] = user_data.get('token')
    session.permanent = True

def clear_session_data() -> None:
    """Clear all session data"""
    session.clear()