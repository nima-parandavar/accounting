import uuid
from decimal import Decimal
from core.models import BaseDateTime, BaseModel, BaseSoftDelete
from sqlmodel import Field, Column, Relationship
from sqlalchemy import String, Integer, Numeric, CheckConstraint
from finance.models import CreditCard


class Unit(BaseModel, BaseSoftDelete, table=True):
    name: str = Field(sa_column=Column(String(250), nullable=False))
    products: list["Product"] = Relationship(back_populates="unit")


class Price(BaseModel, BaseDateTime, table=True):
    price: Decimal = Field(sa_column=Column(Numeric(18, 0), nullable=False))

    __table_args__ = (CheckConstraint("price >= 0", name="chk_price_postive"),)


class Product(BaseModel, BaseDateTime, BaseSoftDelete, table=True):
    name: str = Field(sa_column=Column(String(150), nullable=True))
    code: int = Field(sa_column=Column(Integer(), unique=True))
    stock: int = Field(default=0)

    # fks
    unit_id: uuid.UUID = Field(foreign_key="unit.id", nullable=False)
    unit: Unit = Relationship(back_populates="products")

    purchase_price_id: uuid.UUID = Field(foreign_key="price.id", nullable=False)
    purchase_price: Price = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Product.purchase_price_id]"}
    )

    selling_price_id: uuid.UUID = Field(foreign_key="price.id", nullable=False)
    selling_price: Price = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Product.selling_price_id]"}
    )

    __table_args__ = (
        CheckConstraint(
            "selling_price_id >= purchase_price_id",
            name="chk_selling_gte_purchase",
        ),
    )


class Purchase(BaseModel, BaseDateTime, table=True):
    code: int = Field(unique=True, index=True, nullable=False)
    total_quantity: int = Field(default=1)
    total_price: Decimal = Field(sa_column=Column(Numeric(18, 0), nullable=False))
    is_acceptable: bool = Field(default=False)

    # fks
    items: list["Item"] = Relationship(back_populates="purchase")
    
    credit_card_id: uuid.UUID = Field(foreign_key="creditcard.id")
    credit_card: CreditCard = Relationship(back_populates="purchases")

    __table_args__ = (
        CheckConstraint("total_price > 0", "chk_total_price_positive"),
        CheckConstraint("total_quantity > 0", "chk_total_quantity"),
    )


class Item(BaseModel, table=True):
    product_id: uuid.UUID = Field(foreign_key="product.id", nullable=False)
    product: Product = Relationship()

    quantity: int = Field(default=1)
    price: Decimal = Field(sa_column=Column(Numeric(18, 0), nullable=False))

    purchase_id: uuid.UUID = Field(foreign_key="purchase.id")
    purchase: Purchase = Relationship(back_populates="items")

    __table_args__ = (
        CheckConstraint("price > 0", "chk_price_positive"),
        CheckConstraint("quantity > 0", "chk_quantity"),
    )
