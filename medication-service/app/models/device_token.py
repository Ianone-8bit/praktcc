# ============ FILE: medication-service/app/models/device_token.py ============
from sqlalchemy import Column, Integer, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
from app.services.db import Base


class DeviceToken(Base):
    __tablename__ = "device_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    token = Column(String(512), nullable=False, unique=True)
    platform = Column(String(50), nullable=False, default="unknown")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    __table_args__ = (UniqueConstraint("token", name="uq_device_token"),)
