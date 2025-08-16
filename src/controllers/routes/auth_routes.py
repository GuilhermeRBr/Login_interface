from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from src.schemas.schemas import UserSchemas, LoginSchemas
from src.models.user import User
from src.dependencies.get_db import get_session
from src.config.security import bcrypt_context, authenticate_user, create_token


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
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=401, detail='Email ou senha incorretos')
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, duration=timedelta(days=7))
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"}
    
@auth_router.post('/forgot-password')
async def forgot_password(email: str, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    
    # Aqui você pode implementar a lógica para enviar o e-mail de redefinição de senha
    # Por exemplo, gerar um código de verificação e enviá-lo por e-mail
    
    return {"message": "E-mail de redefinição de senha enviado com sucesso"}