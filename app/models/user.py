import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email           = Column(String, unique=True, index=True, nullable=False)
    # fullname        = Column(String, nullable=False)
    # username        = Column(String, unique=True, index=True, nullable=False)
    password_hash   = Column(String, nullable=False)
    # position        = Column(String, nullable=False)
    # initial_position= Column(String, nullable=False)    
    # level           = Column(Integer, nullable=False)
    # division        = Column(String, nullable=False)
    # department      = Column(String, nullable=False)
    # placement       = Column(String, nullable=False)
    # branch_code     = Column(String, nullable=False)
    # phone_number    = Column(String, nullable=False)
    # email_department_head = Column(String, nullable=True)
    face_encoding   = Column(ARRAY(Float), nullable=True)
    face_registered = Column(Boolean, default=False)
    is_active       = Column(Boolean, default=True)
    # nik             = Column(String, unique=True, index=True, nullable=False)
    # nik_old         = Column(String, unique=True, index=True, nullable=False)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())