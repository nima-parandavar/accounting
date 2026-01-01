import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime, Column
from sqlalchemy.sql import func




class BaseModel(SQLModel, Table=False):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    

class BaseDateTime(SQLModel, Table=False):
    created_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=True,
        ),
    )
    updated_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            server_onupdate=func.now(),
            nullable=True,
        ),
    )


class BaseSoftDelete(SQLModel, Table=False):
    deleted_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    def is_deleted(self):
        return self.deleted_at is not None

    def soft_delete(self):
        self.deleted_at = datetime.now()

    def restore(self):
        self.deleted_at = None
