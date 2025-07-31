import os
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from src.schemas.schemas import UserSchemas, LoginSchemas
from src.models.user import User
from src.dependencies.get_db import get_session
from src.utils.generate_token import create_token

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
async def register(usuario_schema: UserSchemas, session: Session = Depends(get_session)):
    '''Rota de registro'''
    try:
        if session.query(User).filter(User.email == usuario_schema.email).first():
            raise HTTPException(status_code=400, detail='E-mail do usuário já cadastrado')
        else:
            password_encrypted = bcrypt_context.hash(usuario_schema.password)
            new_user = User(usuario_schema.email, password_encrypted)
            session.add(new_user)
            session.commit()
            return {"message": "User registered successfully"}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    

@auth_router.post('/login')
async def login(login_schema: LoginSchemas, session = Depends(get_session)):
    user = session.query(User).filter(User.email == login_schema.email).first()
    if not user:
        raise HTTPException(status_code=400, detail='Usuário não encontrado')
    else:
        access_token = create_token(user.email)
        return {"access_token": access_token,
                "token_type": "Bearer"}