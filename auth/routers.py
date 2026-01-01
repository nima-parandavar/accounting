from fastapi import APIRouter
from config.db import SessionType
from .authorization import AuthFormType

router = APIRouter()


@router.post("/token")
async def login(form: AuthFormType, session: SessionType):
    
    return  