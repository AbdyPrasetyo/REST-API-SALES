from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_user_repository
from app.schemas.auth_schema import RegisterRequest, LoginRequest, LoginResponseStep1, Token
from app.schemas.user_schema import UserResponse
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])

async def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo)

@router.post("/register", response_model=UserResponse)
async def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.register_user(data)

@router.post("/login", response_model=LoginResponseStep1)
async def login(
    data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.authenticate_user_step1(email=data.email, password=data.password)

@router.post("/register-face")
async def register_face(
    email: str = Form(...),
    image: UploadFile = File(...),
    auth_service: AuthService = Depends(get_auth_service)
):
    image_bytes = await image.read()
    return await auth_service.register_face(email=email, image_bytes=image_bytes)

@router.post("/face-login", response_model=Token)
async def face_login(
    email: str = Form(...),
    image: UploadFile = File(...),
    auth_service: AuthService = Depends(get_auth_service)
):
    image_bytes = await image.read()
    return await auth_service.verify_face_login(email=email, image_bytes=image_bytes)
