from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.services.face_service import FaceService
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.schemas.auth_schema import RegisterRequest, LoginResponseStep1, Token
from app.schemas.user_schema import UserResponse
from app.models.user import User

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        
    async def register_user(self, data: RegisterRequest) -> UserResponse:
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
            
        hashed_password = hash_password(data.password)
        new_user = User(
            email=data.email,
            password_hash=hashed_password,
            jabatan=data.jabatan,
            face_registered=False,
            is_active=True
        )
        created_user = await self.user_repo.create(new_user)
        return UserResponse.model_validate(created_user)
        
    async def authenticate_user_step1(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
            
        if not user.face_registered:
            return LoginResponseStep1(require_face_registration=True)
            
        return LoginResponseStep1(require_face_scan=True)
        
    async def register_face(self, email: str, image_bytes: bytes) -> dict:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
        if user.face_registered:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Face already registered")
            
        face_encoding = FaceService.get_face_encoding(image_bytes)
        await self.user_repo.update_face_encoding(user, face_encoding)
        
        return {"message": "Face registered successfully"}
        
    async def verify_face_login(self, email: str, image_bytes: bytes) -> Token:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            
        if not user.face_registered or not user.face_encoding:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Face not registered")
            
        is_match = FaceService.verify_face(user.face_encoding, image_bytes, tolerance=0.45)
        
        if not is_match:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Face not matched")
            
        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
        refresh_token = create_refresh_token(data={"sub": str(user.id), "email": user.email})
        
        return Token(access_token=access_token, refresh_token=refresh_token)