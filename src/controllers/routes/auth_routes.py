from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from src.schemas.schemas import UserSchemas, LoginSchemas
from src.models.user import User
from src.dependencies.get_db import get_session
from src.config.security import bcrypt_context, authenticate_user, create_token


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
async def register(user_schema: UserSchemas, session: Session = Depends(get_session)):
    if session.query(User).filter(User.email == user_schema.email).first():
        raise HTTPException(status_code=400, detail='E-mail do usuário já cadastrado')
    try:
        password_encrypted = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.email, password_encrypted)
        session.add(new_user)
        session.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail='Erro ao registrar usuário')

    
@auth_router.post('/login')
async def login(login_schema: LoginSchemas, session = Depends(get_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=401, detail='Email ou senha incorretos')
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, duration=timedelta(days=7))
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"}
    
@auth_router.post('/reset_password')
async def reset_password(user_schema: UserSchemas, session: Session = Depends(get_session)):

    user = session.query(User).filter(User.email == user_schema.email).first()
    if not user:
        raise HTTPException(status_code=404, detail='Email não encontrado')
    
    try:
        password_encrypted = bcrypt_context.hash(user_schema.password)
        user.password = password_encrypted
        session.commit()
        return {"message": "Password updated successfully"}
            
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail='Erro ao atualizar senha')
