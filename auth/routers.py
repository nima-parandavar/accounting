from fastapi import APIRouter
from .authorization import AuthFormType, AuthType

router = APIRouter()


@router.post("/token")
async def login(token: AuthType, form: AuthFormType):
    return  