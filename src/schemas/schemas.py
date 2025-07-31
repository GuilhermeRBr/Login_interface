from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserSchemas(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(
        orm_mode=True
    )

class LoginSchemas(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(
        orm_mode=True
    )