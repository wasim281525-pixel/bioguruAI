import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.user import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(200))
    language = Column(String(20))
    chapter = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"))
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(20))
    sources = Column(ARRAY(Text))
    tokens_used = Column(Integer)
    latency_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
