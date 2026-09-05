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
from sqlalchemy.orm import relationship, synonym
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.base import Base

# Valid User Roles Constants
ROLE_FARMER = "FARMER"
ROLE_BUYER = "BUYER"
ROLE_ADMIN = "ADMIN"
VALID_ROLES = [ROLE_FARMER, ROLE_BUYER, ROLE_ADMIN]


class RoleString(str):
    """Case-insensitive string representation for roles to bridge DB and API layers."""
    def __eq__(self, other):
        if isinstance(other, str):
            return self.lower() == other.lower()
        return super().__eq__(other)

    def __hash__(self):
        return hash(self.lower())


def utc_now():
    """Helper to return current UTC timestamp."""
    return datetime.now(timezone.utc)


class User(Base):
    """
    User Model Architecture
    Stores primary user accounts (FARMER, BUYER, ADMIN).
    Matches database/schema.sql users table.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=True, index=True)
    phone = Column("phone", String(20), unique=True, nullable=False, index=True)
    phone_number = synonym("phone")
    password_hash = Column(String(255), nullable=False)
    _role = Column("role", Enum("farmer", "buyer", "admin", name="user_roles"), nullable=False, index=True)
    district = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

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
    audit_logs = relationship("AuditLog", back_populates="user", foreign_keys="AuditLog.user_id")

    def get_role(self):
        return RoleString(self._role) if self._role else None

    def set_role(self, value):
        if value:
            self._role = str(value).lower()
        else:
            self._role = value

    role = synonym("_role", descriptor=property(get_role, set_role))

    @property
    def is_verified(self):
        if self.farmer_profile:
            return self.farmer_profile.verification_status == "verified"
        if self.buyer_profile:
            return self.buyer_profile.verification_status == "verified"
        return getattr(self, "_is_verified", False)

    @is_verified.setter
    def is_verified(self, value):
        self._is_verified = bool(value)

    def set_password(self, password: str):
        """Hashes password securely using Werkzeug."""
        if not password or len(str(password).strip()) == 0:
            raise ValueError("Password cannot be empty")
        self.password_hash = generate_password_hash(str(password))

    def check_password(self, password: str) -> bool:
        """Verifies password hash securely using Werkzeug."""
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, str(password))

    def to_dict(self, include_profile=True):
        """
        Converts user object to dictionary for API responses.
        Excludes password and password_hash for security.
        """
        role_str = self.role.upper() if self.role else None
        data = {
            "id": self.id,
            "full_name": self.full_name,
            "phone": self.phone,
            "phone_number": self.phone,
            "email": self.email,
            "role": role_str,
            "district": self.district,
            "state": self.state,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_profile:
            if role_str == ROLE_FARMER and self.farmer_profile:
                data["profile"] = self.farmer_profile.to_dict()
            elif role_str == ROLE_BUYER and self.buyer_profile:
                data["profile"] = self.buyer_profile.to_dict()
            elif role_str == ROLE_ADMIN and self.admin_profile:
                data["profile"] = self.admin_profile.to_dict()
            else:
                data["profile"] = None

        return data


class FarmerProfile(Base):
    """
    Farmer Profile Model
    Linked to a FARMER user account. Matches database/schema.sql farmer_profiles table.
    """
    __tablename__ = "farmer_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    farm_name = Column(String(150), nullable=True)
    crop_types = Column(Text, nullable=True)
    primary_crops = synonym("crop_types")
    land_area = Column(Numeric(10, 2), nullable=True)
    farm_size_acres = synonym("land_area")
    location = Column(String(255), nullable=True)
    verification_status = Column(String(50), default="pending", nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    user = relationship("User", back_populates="farmer_profile")

    def to_dict(self):
        land_area_val = float(self.land_area) if self.land_area is not None else None
        return {
            "id": self.id,
            "user_id": self.user_id,
            "farm_name": self.farm_name,
            "crop_types": self.crop_types,
            "primary_crops": self.crop_types,
            "land_area": land_area_val,
            "farm_size_acres": land_area_val,
            "location": self.location,
            "verification_status": self.verification_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class BuyerProfile(Base):
    """
    Buyer Profile Model
    Linked to a BUYER user account. Matches database/schema.sql buyer_profiles table.
    """
    __tablename__ = "buyer_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    business_name = Column(String(150), nullable=True)
    business_type = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)
    verification_status = Column(String(50), default="pending", nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(
        DateTime, default=utc_now, onupdate=utc_now, nullable=False
    )

    user = relationship("User", back_populates="buyer_profile")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "business_name": self.business_name,
            "business_type": self.business_type,
            "location": self.location,
            "verification_status": self.verification_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class AdminProfile(Base):
    """
    Admin Profile Model
    Linked to an ADMIN user account. Matches database/schema.sql admin_profiles table.
    """
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

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "department": self.department,
            "permissions": self.permissions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class AuditLog(Base):
    """
    Audit Log Model
    Tracks administrative and system actions. Matches database/schema.sql audit_logs table.
    """
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    admin_id = synonym("user_id")
    action = Column(String(100), nullable=False)
    entity_type = Column(String(100), nullable=True)
    entity_id = Column(Integer, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False, index=True)

    user = relationship("User", back_populates="audit_logs", foreign_keys=[user_id])

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "admin_id": self.user_id,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


AdminActivity = AuditLog
