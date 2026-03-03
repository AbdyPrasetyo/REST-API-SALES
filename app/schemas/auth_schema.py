from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    jabatan: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponseStep1(BaseModel):
    require_face_registration: bool = False
    require_face_scan: bool = False

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"