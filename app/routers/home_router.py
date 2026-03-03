from fastapi import APIRouter
from app.controllers.home_controller import HomeController

router = APIRouter()


@router.get("/home")
def home():
    controller = HomeController()
    return controller.home()