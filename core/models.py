import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy.sql import func




class BaseModel(SQLModel, table=False):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    

class BaseDateTime(SQLModel, table=False):

    created_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": func.now(),
            "nullable":True,
        },
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": func.now(),
            "server_onupdate":func.now(),
            "nullable":True,
        }
    )


class BaseSoftDelete(SQLModel, table=False):

    deleted_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={"nullable":True,},
    )

    def is_deleted(self):
        return self.deleted_at is not None

    def soft_delete(self):
        self.deleted_at = datetime.now()

    def restore(self):
        self.deleted_at = None
