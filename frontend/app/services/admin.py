"""Admin service module"""
from typing import List, Dict, Optional
from .base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__('/api/admin')

    def get_users(self) -> List[Dict]:
        """Get all users"""
        result = self._handle_request('get', f"{self.endpoint}/users/")
        return result if result else []

    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get a specific user"""
        users = self.get_users()
        return next((user for user in users if user['email'] == user_id), None)

    def create_user(self, user_data: Dict) -> Optional[Dict]:
        """Create a new user and assign preset accounts if specified"""
        # Handle preset_id conversion
        if 'preset_id' in user_data:
            try:
                user_data['preset_id'] = int(user_data['preset_id'])
                if user_data['preset_id'] == 0:
                    del user_data['preset_id']
            except (ValueError, TypeError):
                del user_data['preset_id']

        # Create the user
        created_user = self._handle_request('post', f"{self.endpoint}/users/", user_data)
        return created_user

    def update_user(self, user_id: str, user_data: Dict) -> Optional[Dict]:
        """Update an existing user"""
        # Handle preset_id conversion
        if 'preset_id' in user_data:
            try:
                user_data['preset_id'] = int(user_data['preset_id'])
                if user_data['preset_id'] == 0:
                    del user_data['preset_id']
            except (ValueError, TypeError):
                del user_data['preset_id']

        # Update the user
        updated_user = self._handle_request('put', f"{self.endpoint}/users/{user_id}", user_data)
        return updated_user

    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        result = self._handle_request('delete', f"{self.endpoint}/users/{user_id}")
        return bool(result)

    def get_user_accounts(self, user_id: str) -> List[Dict]:
        """Get accounts assigned to a user"""
        result = self._handle_request('get', f"{self.endpoint}/users/{user_id}/accounts")
        return result if result else []

    def get_available_accounts(self) -> List[Dict]:
        """Get all available accounts"""
        result = self._handle_request('get', f"{self.endpoint}/accounts/")
        return result if result else []

    def assign_account_to_user(self, user_id: str, account_id: int) -> bool:
        """Assign an account to a user"""
        result = self._handle_request(
            'post', 
            f"{self.endpoint}/users/{user_id}/accounts/{account_id}"
        )
        return bool(result)

    def remove_account_from_user(self, user_id: str, account_id: int) -> bool:
        """Remove an account from a user"""
        result = self._handle_request(
            'delete', 
            f"{self.endpoint}/users/{user_id}/accounts/{account_id}"
        )
        return bool(result)

    def get_analytics(self) -> Dict:
        """Get analytics dashboard data"""
        result = self._handle_request('get', f"{self.endpoint}/analytics/")
        return result if result else {}

    def get_user_analytics(self, user_id: str) -> Dict:
        """Get analytics for a specific user"""
        result = self._handle_request('get', f"{self.endpoint}/analytics/user/{user_id}")
        return result if result else {}

    def get_account_analytics(self, account_id: int) -> Dict:
        """Get analytics for a specific account"""
        result = self._handle_request('get', f"{self.endpoint}/analytics/account/{account_id}")
        return result if result else {}

    def get_presets(self) -> List[Dict]:
        """Get all presets"""
        result = self._handle_request('get', f"{self.endpoint}/presets/")
        return result if result else []

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        """Get a specific preset"""
        result = self._handle_request('get', f"{self.endpoint}/presets/{preset_id}")
        return result

    def create_preset(self, preset_data: Dict) -> Optional[Dict]:
        """Create a new preset"""
        return self._handle_request('post', f"{self.endpoint}/presets/", preset_data)

    def update_preset(self, preset_id: int, preset_data: Dict) -> Optional[Dict]:
        """Update an existing preset"""
        return self._handle_request('put', f"{self.endpoint}/presets/{preset_id}", preset_data)

    def delete_preset(self, preset_id: int) -> bool:
        """Delete a preset"""
        result = self._handle_request('delete', f"{self.endpoint}/presets/{preset_id}")
        return bool(result)