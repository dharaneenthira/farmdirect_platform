"""
Product & Inventory SQLAlchemy ORM Model
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from backend.models.base import Base


def utc_now():
    """Helper to return current UTC timestamp."""
    return datetime.now(timezone.utc)


class Product(Base):
    """
    SQLAlchemy ORM Model representing the products table in MySQL schema.
    Matches database/schema.sql products definition exactly.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    farmer_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(150), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    quantity = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(20), default="kg", nullable=False)
    asking_price = Column(Numeric(10, 2), nullable=False)
    location = Column(String(255), nullable=True)
    status = Column(String(50), default="active", nullable=False, index=True)
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
    farmer = relationship("User", back_populates="products")

    def to_dict(self):
        """
        Converts product object to dictionary for API responses.
        Uses only existing User model fields (id, full_name, email, phone, district, state).
        """
        data = {
            "id": self.id,
            "farmer_id": self.farmer_id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "quantity": float(self.quantity) if self.quantity is not None else 0.0,
            "unit": self.unit,
            "asking_price": float(self.asking_price) if self.asking_price is not None else 0.0,
            "location": self.location,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if self.farmer:
            farmer_data = {
                "id": self.farmer.id,
                "full_name": self.farmer.full_name,
                "email": self.farmer.email,
                "phone": self.farmer.phone,
                "district": self.farmer.district,
                "state": self.farmer.state,
            }
            if hasattr(self.farmer, "farmer_profile") and self.farmer.farmer_profile:
                farmer_data["farm_name"] = self.farmer.farmer_profile.farm_name
            data["farmer"] = farmer_data
        return data
