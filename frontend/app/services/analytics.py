from typing import Dict
from .base_service import BaseService

class AnalyticsService(BaseService):
    def __init__(self):
        super().__init__('/api/analytics')
    
    def get_user_analytics(self, user_id: str) -> Dict:
        result = self._handle_request('get', f"{self.endpoint}/user/{user_id}")
        return result if result else {}
    
    def get_account_analytics(self, account_id: int) -> Dict:
        result = self._handle_request('get', f"{self.endpoint}/account/{account_id}")
        return result if result else {}
        
    def get_dashboard_analytics(self) -> Dict:
        result = self._handle_request('get', '/api/admin/analytics')
        return result if result else {
            'accounts': [],
            'recent_activity': []
        }