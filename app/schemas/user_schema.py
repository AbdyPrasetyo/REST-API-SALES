from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    jabatan: Optional[str] = None
    face_registered: bool = False
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True