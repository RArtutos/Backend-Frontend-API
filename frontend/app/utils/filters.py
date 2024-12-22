"""Template filters for the application"""
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

def register_filters(app):
    """Register all template filters"""
    app.jinja_env.filters['datetime'] = format_datetime