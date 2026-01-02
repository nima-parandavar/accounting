import uuid
from core.jwt import JWT
from config.db import SessionType
from sqlalchemy import select
from .models import User
from .authorization import AuthFormType
from fastapi.exceptions import HTTPException
from fastapi import status
from .schemas import LoginUserResponse
from datetime import timedelta, datetime
from config.settings import app_settings


async def login_user(session: SessionType, body: AuthFormType):
    """
    create access token for user to login
    """
    jwt = JWT()
    async with session as ses:
        statement = select(User).where(
            User.email == body.username,
        )
        results = await ses.exec(statement)
        user: User | None = results.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User or password is wrong",
            )
        if not user.check_password(body.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User or password is wrong",
            )
    payload = {
        "id": str(user.id),
        "exp": (datetime.now()
        + timedelta(minutes=app_settings.access_token_expire_minutes)).timestamp(),
    }
    token = jwt.encode(payload)
    return LoginUserResponse(token=token, token_type="bearer")


async def get_current_user_info(session: SessionType, user_id: str) -> User:
    async with session as ses:
        user: User | None = await ses.get(User, uuid.UUID(user_id))

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user