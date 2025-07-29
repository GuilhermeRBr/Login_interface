from fastapi import APIRouter, Depends
from src.models.user import User
from src.dependencies.get_db import get_session


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register")
async def register(email: str, password: str, session = Depends(get_session)):
    '''Rota de registro'''
    try:
        if session.query(User).filter(User.email == email).first():
            return {"message": "Email already registered"}
        
        new_user = User(email=email, password=password)
        session.add(new_user)
        session.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}
    finally:
        session.close()