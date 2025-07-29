from typing import Dict, Optional
from sqlalchemy import create_engine, Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db = create_engine('sqlite:///storage/data/database.db', echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=db, autoflush=False, autocommit=False)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f"<User(email='{self.email}')>"

    
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
    
