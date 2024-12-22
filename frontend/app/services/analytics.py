from typing import Dict
from .base_service import BaseService

class AnalyticsService(BaseService):
    def __init__(self):
        super().__init__('/api/analytics')
    
    def get_user_analytics(self, user_id: str) -> Dict:
        result = self._handle_request('get', f"{self.endpoint}/user/{user_id}")
        if result:
            # Asegurar valores por defecto
            result.setdefault('current_sessions', 0)
            result.setdefault('total_time', 0)
            result.setdefault('total_sessions', 0)
            result.setdefault('account_usage', [])
            result.setdefault('last_activities', [])
        return result or {}
    
    def get_account_analytics(self, account_id: int) -> Dict:
        result = self._handle_request('get', f"{self.endpoint}/account/{account_id}")
        if result:
            # Asegurar valores por defecto
            result.setdefault('total_users', 0)
            result.setdefault('active_users', 0)
            result.setdefault('total_sessions', 0)
            result.setdefault('current_sessions', 0)
            result.setdefault('max_concurrent_users', 1)  # Valor por defecto
            result.setdefault('usage_by_domain', [])
            result.setdefault('user_activities', [])
        return result or {}
        
    def get_dashboard_analytics(self) -> Dict:
        result = self._handle_request('get', '/api/admin/analytics')
        if result:
            # Asegurar valores por defecto para cada cuenta
            for account in result.get('accounts', []):
                account.setdefault('max_concurrent_users', 1)
                account.setdefault('active_sessions', 0)
                account.setdefault('total_users', 0)
                account.setdefault('active_users', 0)
        return result or {
            'accounts': [],
            'recent_activity': []
        }
