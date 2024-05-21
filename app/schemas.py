from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone


def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


class WorkBase(BaseModel):
    name: str
    tree_id: int
    start_date: datetime = Field(default_factory=datetime_now)
    end_date: datetime = Field(default_factory=datetime_now)
    parent_id: UUID = Field(default=None)


class WorkCreate(WorkBase):
    pass


class Work(WorkBase):
    id: UUID = Field(default_factory=uuid4)
    is_deleted: bool = False

    class Config:
        orm_mode = True
