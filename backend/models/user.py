import uuid
from sqlalchemy import Column, String, SmallInteger, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password_hash = Column(Text, nullable=False)
    class_level = Column(SmallInteger, default=11)
    language = Column(String(20), default="en")
    role = Column(String(20), default="student")
    streak_days = Column(Integer, default=0)
    last_active = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
