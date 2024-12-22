from typing import List, Dict, Optional
from .base_service import BaseService

class ProxyService(BaseService):
    def __init__(self):
        super().__init__('/api/proxies')
    
    def get_all(self) -> List[Dict]:
        result = self._handle_request('get', self.endpoint)
        return result if result else []
    
    def create(self, data: Dict) -> Optional[Dict]:
        return self._handle_request('post', self.endpoint, data)