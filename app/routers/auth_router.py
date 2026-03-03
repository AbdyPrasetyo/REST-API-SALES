from fastapi import APIRouter, Depends, UploadFile, File
from app.controllers.auth_controller import AuthController
from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(payload: RegisterRequest, controller: AuthController = Depends()):
    return controller.register(payload)


@router.post("/login")
async def login(
    payload: LoginRequest,
    face_file: UploadFile = File(None),   
    controller: AuthController = Depends()
):
    face_bytes = None
    if face_file:
        face_bytes = await face_file.read()

    return controller.login(payload, face_bytes)