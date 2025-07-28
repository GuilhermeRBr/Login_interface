from fastapi import APIRouter
from src.models.user import User


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register")
async def register():
    '''Rota de registro'''

    return {"message": f" registrado com sucesso!"}