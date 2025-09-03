import os
from typing import Dict, Optional
from sqlalchemy import create_engine, Column, String, Integer, DateTime, func
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

db = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


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

    

