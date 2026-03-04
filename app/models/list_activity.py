import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, JSON, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from app.db.session import Base

class ListActivity(Base):
    __tablename__   = "list_activity"
    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email_sales     = Column(String, nullable=False)
    year            = Column(Integer, nullable=False)
    month           = Column(String, nullable=False)
    week            = Column(Integer, nullable=False)
    day             = Column(String, nullable=False)
    efective_day    = Column(Date, nullable=False)
    data_mitra      = Column(JSON, nullable=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    updated_at      = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())