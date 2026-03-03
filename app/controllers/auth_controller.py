from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas.auth_schema import RegisterRequest, LoginRequest


class AuthController:

    def __init__(self, db: Session = Depends(get_db)):
        self.repo = UserRepository(db)
        self.service = AuthService(self.repo)

    def register(self, payload: RegisterRequest):
        return self.service.register(payload.email, payload.password)

    def login(self, payload: LoginRequest):
        result = self.service.login(payload.email, payload.password)
        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return result