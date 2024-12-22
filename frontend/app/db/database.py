import json
from datetime import datetime
from typing import Optional, List, Dict
from ..core.config import settings
from ..core.auth import get_password_hash

class Database:
    def __init__(self):
        self.file_path = settings.DATA_FILE

    def _read_data(self) -> dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_data(self, data: dict):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    # User methods
    def get_users(self) -> List[Dict]:
        data = self._read_data()
        users = data.get("users", [])
        
        # Add required fields and process data
        for user in users:
            # Convert string timestamps to datetime objects
            if isinstance(user.get("created_at"), str):
                user["created_at"] = datetime.fromisoformat(user["created_at"])
            if user.get("expires_at") and isinstance(user["expires_at"], str):
                user["expires_at"] = datetime.fromisoformat(user["expires_at"])
            
            # Add is_active field based on expiration
            user["is_active"] = True
            if user.get("expires_at"):
                user["is_active"] = datetime.utcnow() < user["expires_at"]
            
            # Add assigned_accounts field
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data.get("user_accounts", [])
                if ua["user_id"] == user["email"]
            ]
        
        return users