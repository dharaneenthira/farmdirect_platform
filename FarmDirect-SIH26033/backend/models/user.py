from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.base import Base

# Valid User Roles
ROLE_FARMER = "FARMER"
ROLE_BUYER = "BUYER"
ROLE_ADMIN = "ADMIN"
VALID_ROLES = [ROLE_FARMER, ROLE_BUYER, ROLE_ADMIN]


class User(Base):
    """
    User Model Architecture
    Stores primary user accounts (FARMER, BUYER, ADMIN).
    Passwords are encrypted securely using Werkzeug password hashing.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    # One-to-One Relationships
    farmer_profile = relationship(
        "FarmerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    buyer_profile = relationship(
        "BuyerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        """Securely hashes plaintext password using Werkzeug"""
        if not password or len(password.strip()) == 0:
            raise ValueError("Password cannot be empty")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies candidate password against stored Werkzeug hash"""
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_profile=True):
        """
        Returns dictionary representation of User object.
        CRITICAL SECURITY: password and password_hash are strictly EXCLUDED.
        """
        data = {
            "id": self.id,
            "full_name": self.full_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "role": self.role,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_profile:
            if self.role == ROLE_FARMER and self.farmer_profile:
                data["profile"] = self.farmer_profile.to_dict()
            elif self.role == ROLE_BUYER and self.buyer_profile:
                data["profile"] = self.buyer_profile.to_dict()
            else:
                data["profile"] = None

        return data


class FarmerProfile(Base):
    """
    Farmer Profile Architecture
    Detailed agricultural profile linked to a FARMER user account.
    """
    __tablename__ = "farmer_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    location = Column(String(255), nullable=True)
    farm_size_acres = Column(Float, nullable=True)
    primary_crops = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    user = relationship("User", back_populates="farmer_profile")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "location": self.location,
            "farm_size_acres": self.farm_size_acres,
            "primary_crops": self.primary_crops,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class BuyerProfile(Base):
    """
    Buyer Profile Architecture
    Detailed purchasing profile linked to a BUYER user account.
    """
    __tablename__ = "buyer_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    business_name = Column(String(255), nullable=True)
    business_type = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


    user = relationship("User", back_populates="buyer_profile")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "business_name": self.business_name,
            "business_type": self.business_type,
            "location": self.location,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class AdminActivity(Base):
    """
    Admin Activity Audit Architecture
    Audit log tracking administrative actions and logins.
    """
    __tablename__ = "admin_activity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action = Column(String(255), nullable=False)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    admin = relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "admin_id": self.admin_id,
            "action": self.action,
            "ip_address": self.ip_address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


