from core.models import BaseDateTime, BaseModel, BaseSoftDelete
from sqlmodel import Field, Column, SQLModel


class Unit(SQLModel, BaseModel, BaseSoftDelete, table=True):
    pass

class Price(SQLModel, BaseModel, BaseDateTime, table=True):
    pass


class Product(SQLModel, BaseModel, BaseDateTime, BaseSoftDelete, table=True):
    pass


class Item(SQLModel, BaseModel, table=True):
    pass


class Purchase(SQLModel, BaseModel, BaseDateTime, table=True):
    pass