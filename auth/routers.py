from fastapi import APIRouter
from config.db import SessionType
from .authorization import AuthFormType, CurrentUserType
from .schemas import LoginUserResponse, UserResponse
from .operations import login_user, get_current_user_info

router = APIRouter()


@router.post(
    "/token",
    response_model=LoginUserResponse,
    status_code=200,
    response_description="User login successfully",
)
async def login(form: AuthFormType, session: SessionType):
    result = await login_user(session, form)
    return result


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=200,
    description="get current user info",
)
async def get_current_user(current_user: CurrentUserType, session: SessionType):
    user = await get_current_user_info(session=session, user_id=current_user)
    return UserResponse(**user.model_dump())
