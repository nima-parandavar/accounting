from datetime import datetime
from enum import Enum
import uuid
from decimal import Decimal
from core.models import BaseDateTime, BaseModel, BaseSoftDelete
from sqlmodel import SQLModel, Numeric, Field, Column, Relationship, Enum as SaEnum


class PaymentMethod(str, Enum):
    CASH = 'cash'
    POS_DEVICE = 'pos_device'
    ONLINE = 'online'
    TRANSFER = 'transfer'

class Service(SQLModel, BaseModel, BaseDateTime, BaseSoftDelete, table=True):
    name: str
    price: Decimal = Field(sa_column=Column(Numeric(18, 0), nullable=False))
    payment_method: Enum = Field(sa_column=Column(SaEnum(PaymentMethod), nullable=False))
    is_payed: bool = Field(default=False)


class Sale(BaseModel, BaseDateTime):
    items: list["SaleItem"] = Relationship(back_populates="sale")
    total_price: Decimal = Field(sa_column=Column(Numeric(18, 0), nullable=False))
    total_quntity: int



class SaleItem(BaseModel):
    service_id: uuid.UUID = Field(foreign_key="service.id")
    service: Service = Relationship(back_populates="service")

    sale_id: uuid.UUID = Field(foreign_key="sale.id")
    sale: Sale = Relationship(back_populates="items")

    quantity: int = Field(default=1)
    price: Decimal = Field(sa_column=Column(Numeric(18, 0), nullable=False))