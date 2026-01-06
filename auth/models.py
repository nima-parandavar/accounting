import enum
from sqlmodel import Relationship
from core.models import BaseModel
from core.regex import phone_number_rgx
from core.hash import Hash
from pydantic import EmailStr, Field
from sqlalchemy import Column, String, Enum as SaEnum
from sqlalchemy.orm import validates
from core.utils import normalize_phone_number


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


class User(BaseModel, table=True):
    email: EmailStr = Field(unique=True, index=True)
    phone_number: str = Field(
        pattern=phone_number_rgx,
        unique=True,
        index=True,
    )

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

    # fks
    credit_cards: list["CreditCard"] = Relationship(back_populates="user")
    pos_devices: list["POSDevice"] = Relationship(back_populates="user")


    def make_password(self, password: str):
        hash_handler = Hash()
        return hash_handler.make_hash(password)

    def verify_password(self, raw_password: str, hash_password):
        hash_handler = Hash()
        return hash_handler.verify(hash_password, raw_password)

    def set_password(self, password: str):
        self.password = self.make_password(password)

    def check_password(self, raw_password):
        return self.verify_password(raw_password, self.password)

    @validates("phone_number")
    def normalize_phone(self, key, value: str):
        return normalize_phone_number(value)
