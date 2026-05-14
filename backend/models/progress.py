import uuid
from sqlalchemy import Column, String, SmallInteger, Integer, DateTime, Numeric, ForeignKey, ARRAY, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.user import Base


class NEETSession(Base):
    __tablename__ = "neet_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    chapter = Column(String(100))
    total_q = Column(Integer)
    correct = Column(Integer, default=0)
    wrong = Column(Integer, default=0)
    skipped = Column(Integer, default=0)
    score_pct = Column(Numeric(5, 2))
    time_taken = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StudentProgress(Base):
    __tablename__ = "student_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    chapter = Column(String(100), nullable=False)
    class_level = Column(SmallInteger)
    accuracy = Column(Numeric(5, 2), default=0)
    attempts = Column(Integer, default=0)
    weak_topics = Column(ARRAY(String))
    mastery = Column(String(20), default="beginner")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("user_id", "chapter"),)


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uploader_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    filename = Column(String(255))
    source_type = Column(String(50))
    class_level = Column(SmallInteger)
    chapter = Column(String(100))
    chunk_count = Column(Integer, default=0)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    query = Column(String)
    language = Column(String(20))
    chunks_retrieved = Column(Integer)
    top_score = Column(Numeric(5, 4))
    response_latency_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
