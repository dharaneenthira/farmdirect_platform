"""
User & Profile SQLAlchemy ORM Models
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum,
    Text,
    Numeric,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.base import Base


def utc_now():
    """Helper to return current UTC timestamp."""
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=True, index=True)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        Enum("farmer", "buyer", "admin", name="user_roles"),
        nullable=False,
        index=True,
    )
    district = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime, default=utc_now, nullable=False, index=True
    )
    updated_at = Column(
        DateTime,
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    # Relationships
    farmer_profile = relationship(
        "FarmerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    buyer_profile = relationship(
        "BuyerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    admin_profile = relationship(
        "AdminProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    audit_logs = relationship("AuditLog", back_populates="user")

    def set_password(self, password: str):
        """Hashes password securely using Werkzeug."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifies password hash securely using Werkzeug."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Converts user object to dictionary for API responses."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "district": self.district,
            "state": self.state,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class FarmerProfile(Base):
    __tablename__ = "farmer_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    farm_name = Column(String(150), nullable=True)
    crop_types = Column(Text, nullable=True)
    land_area = Column(Numeric(10, 2), nullable=True)
    location = Column(String(255), nullable=True)
    verification_status = Column(String(50), default="pending", nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    user = relationship("User", back_populates="farmer_profile")


class BuyerProfile(Base):
    __tablename__ = "buyer_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    business_name = Column(String(150), nullable=True)
    business_type = Column(String(100), nullable=True)
    verification_status = Column(String(50), default="pending", nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    user = relationship("User", back_populates="buyer_profile")


class AdminProfile(Base):
    __tablename__ = "admin_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    department = Column(String(100), nullable=True)
    permissions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    user = relationship("User", back_populates="admin_profile")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=True)
    entity_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)

    user = relationship("User", back_populates="audit_logs")
