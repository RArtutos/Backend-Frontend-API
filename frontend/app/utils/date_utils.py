"""Utility functions for date handling"""
from datetime import datetime
from typing import Optional

def format_datetime(dt: Optional[datetime | str]) -> str:
    """Format datetime for display"""
    if not dt:
        return "Never"
    
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except (ValueError, TypeError):
            return dt
            
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_expiration_status(expires_at: Optional[datetime]) -> tuple:
    """Get expiration status and appropriate CSS class"""
    if not expires_at:
        return "Never", "success"
    
    now = datetime.utcnow()
    if expires_at < now:
        return "Expired", "danger"
    
    days_left = (expires_at - now).days
    if days_left <= 7:
        return f"Expires in {days_left} days", "warning"
    return f"Expires in {days_left} days", "success"