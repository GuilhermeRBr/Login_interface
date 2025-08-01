from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserSchemas(BaseModel):
    email: str
    password: str

    model_config = {
        "from_attributes": True
    }

class LoginSchemas(BaseModel):
    email: str
    password: str

    model_config = {
        "from_attributes": True
    }