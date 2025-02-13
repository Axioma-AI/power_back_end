from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    picture: Optional[str] = None
    country_code: Optional[str] = None
    email_verified: Optional[bool] = False
