import enum
from core.models import BaseModel
from core.regex import phone_number_rgx
from core.hash import Hash
from pydantic import EmailStr, Field
from sqlalchemy import Column, String, Enum as SaEnum
from sqlalchemy.orm import validates
from config.settings import app_settings


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class User(BaseModel, table=True):
    email: EmailStr = Field(unique=True, index=True)
    phone_number: str = Field(pattern=phone_number_rgx, unique=True, index=True)

    first_name: str = Field(
        sa_column=Column(String(50), nullable=False),
    )
    last_name: str | None = Field(
        sa_column=Column(String(100), nullable=True),
    )

    password: str = Field(sa_column=Column(nullable=False))
    role: UserRole = Field(
        sa_column=Column(
            SaEnum(UserRole, name="user_role_enum"), server_default=UserRole.USER.value
        )
    )

    @property
    def normalize_phone_number(self):
        phone_number = self.phone_number
        if phone_number.startswith("+98") and phone_number[3] == 0:
            phone_number = f"{app_settings.phone_number_region_code}{phone_number[4:]}"
        elif phone_number.startswith("0"):
            phone_number = f"{app_settings.phone_number_region_code}{phone_number[1:]}"

        return phone_number

    def make_password(self, password: str):
        hash_handler = Hash()
        return hash_handler.make_hash(password)
    

    def verify_password(self, raw_password: str, hash_password):
        hash_handler = Hash()
        return hash_handler.verify(hash_password, raw_password)


    def set_password(self, password: str):
        self.password = self.make_password(password)

    # @validates("phone_number")
    # def _normalize_phone(self, key, value):
    #     self.phone_number = value
    #     return self.normalize_phone_number()
