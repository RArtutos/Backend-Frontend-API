from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email: str, is_admin: bool = False):
        self.email = email
        self.is_admin = is_admin
        
    def get_id(self):
        return self.email