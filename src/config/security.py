import os
from jose import jwt, JWTError
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from src.models.user import User


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def authenticate_user(email: str, password: str, session) -> bool:
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_token(user_id, duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration = datetime.now(timezone.utc) + duration
    to_encode = {"exp": expiration, "sub": str(user_id)}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return token