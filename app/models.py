from sqlalchemy import Column, Integer, String, \
    DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .database import Base


class Work(Base):
    __tablename__ = "work"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id = Column(UUID(), ForeignKey('work.id'), nullable=True)
    name = Column(String)
    tree_id = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_deleted = Column(Boolean, default=False)
