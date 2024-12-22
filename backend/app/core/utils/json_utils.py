"""Utility functions for JSON serialization"""
from datetime import datetime
import json
from pydantic.networks import AnyUrl  # Cambiamos HttpUrl por AnyUrl

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects and Pydantic URLs"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, AnyUrl):  # Usamos AnyUrl en lugar de HttpUrl
            return str(obj)
        return super().default(obj)

def serialize_datetime(obj):
    """Convert datetime objects to ISO format strings"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, AnyUrl):  # Usamos AnyUrl en lugar de HttpUrl
        return str(obj)
    return obj
