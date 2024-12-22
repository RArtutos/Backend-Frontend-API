import requests
from typing import Optional, Dict, Any
from flask_login import current_user

class HttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _get_auth(self):
        return (current_user.email, '') if current_user.is_authenticated else None

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        response = requests.get(
            f"{self.base_url}{endpoint}",
            params=params,
            auth=self._get_auth()
        )
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: Dict) -> Dict:
        response = requests.post(
            f"{self.base_url}{endpoint}",
            json=data,
            auth=self._get_auth()
        )
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: Dict) -> Dict:
        response = requests.put(
            f"{self.base_url}{endpoint}",
            json=data,
            auth=self._get_auth()
        )
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> bool:
        response = requests.delete(
            f"{self.base_url}{endpoint}",
            auth=self._get_auth()
        )
        response.raise_for_status()
        return True