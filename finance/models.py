import uuid
from decimal import Decimal
from auth.models import User
from core.models import BaseSoftDelete, BaseDateTime, BaseModel
from sqlalchemy import String, Column, Numeric
from sqlalchemy.orm import validates
from sqlmodel import Field, Relationship
from azbankintro import card_validate, iban_validate


class CreditCard(BaseModel, BaseDateTime, BaseSoftDelete, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="credit_cards")

    name: str = Field(sa_column=Column(String(150), nullable=False))
    card_number: str = Field(sa_column=Column(String(16), unique=True))
    iban: str = Field(unique=True)
    account_number: str = Field(unique=True)
    balance: Decimal  = Field(default=0, sa_column=Column(Numeric(10, 0)))

    # fks
    pos_device: list["POSDevice"] = Relationship(back_populates="credit_card")

    @validates("card_number")
    def validate_card_number(self, key, value: str):
        card_validate(value)
        return value

    @validates("iban")
    def validate_iban(self, key, value: str):
        iban_validate(value)
        return value


class POSDevice(BaseModel, BaseDateTime, BaseSoftDelete, table=True):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="pos_devices")

    credit_card_id: uuid.UUID = Field(foreign_key="creditcard.id")
    credit_card: CreditCard = Relationship(back_populates="pos_device")

    name: str = Field(nullable=False)
    serial_number: str = Field(unique=True)



class Transaction(BaseModel, BaseDateTime, table=True):
    pass