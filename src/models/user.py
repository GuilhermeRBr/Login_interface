from typing import Dict, Optional

class UserModel:
    def __init__(self):
        self.users_db: Dict[str, str] = {}
        self.verification_codes: Dict[str, str] = {}
    
    def user_exists(self, email: str) -> bool:
        return email in self.users_db
    
    def authenticate_user(self, email: str, password: str) -> bool:
        return email in self.users_db and self.users_db[email] == password
    
    def create_user(self, email: str, password: str) -> bool:
        if email in self.users_db:
            return False
        self.users_db[email] = password
        return True
    
    def update_password(self, email: str, new_password: str) -> bool:
        if email not in self.users_db:
            return False
        self.users_db[email] = new_password
        return True
    
    def store_verification_code(self, email: str, code: str):
        self.verification_codes[email] = code
    
    def verify_code(self, email: str, code: str) -> bool:
        return self.verification_codes.get(email) == code