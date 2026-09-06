"""
Automated Test Suite for Database Configuration, Connection, User Models & Password Hashing
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
import pytest
from backend.config import TestingConfig, Config
from backend.db.session import check_db_connection
from backend.models import (
    User,
    FarmerProfile,
    BuyerProfile,
    AdminProfile,
    AuditLog,
)


def test_database_configuration():
    """
    Verify environment database configurations
    """
    assert Config.DB_NAME == "farmdirect_db"
    assert Config.DB_PORT == "3306"
    assert "sqlite" in TestingConfig.SQLALCHEMY_DATABASE_URI
    assert TestingConfig.TESTING is True


def test_database_connection(app):
    """
    Verify database connection status check helper
    """
    assert check_db_connection() is True


def test_password_hashing():
    """
    Verify Werkzeug password hashing and verification methods
    """
    user = User(
        full_name="Security Test User",
        phone="+919000000001",
        email="security@example.com",
        role="farmer",
    )
    plain_password = "SecretPassword2026!"
    user.set_password(plain_password)

    # Password must not be stored as plain text
    assert user.password_hash != plain_password
    assert user.password_hash.startswith("scrypt:") or user.password_hash.startswith("pbkdf2:")

    # Verify password validation
    assert user.check_password(plain_password) is True
    assert user.check_password("WrongPassword") is False


def test_user_creation_and_farmer_role(db_session):
    """
    Verify user creation with farmer role and profile creation
    """
    farmer_user = User(
        full_name="Kannan Farmer",
        email="kannan@farm.com",
        phone="+919876500001",
        role="farmer",
        district="Erode",
        state="Tamil Nadu",
    )
    farmer_user.set_password("FarmerPass2026!")

    db_session.add(farmer_user)
    db_session.commit()

    saved_user = db_session.query(User).filter_by(phone="+919876500001").first()
    assert saved_user is not None
    assert saved_user.full_name == "Kannan Farmer"
    assert saved_user.role == "farmer"

    # Add Farmer Profile
    farmer_profile = FarmerProfile(
        user_id=saved_user.id,
        farm_name="Kannan Agro Farm",
        crop_types="Turmeric, Sugarcane",
        land_area=5.50,
        location="Erode Rural",
        verification_status="verified",
    )
    db_session.add(farmer_profile)
    db_session.commit()

    assert saved_user.farmer_profile is not None
    assert saved_user.farmer_profile.farm_name == "Kannan Agro Farm"


def test_buyer_and_admin_roles(db_session):
    """
    Verify buyer and admin user roles and associated profile creation
    """
    buyer_user = User(
        full_name="Buyer Enterprise",
        email="buyer@enterprise.com",
        phone="+919876500002",
        role="buyer",
        district="Madurai",
        state="Tamil Nadu",
    )
    buyer_user.set_password("BuyerPass2026!")
    db_session.add(buyer_user)

    admin_user = User(
        full_name="Admin Supervisor",
        email="admin@supervisor.com",
        phone="+919876500003",
        role="admin",
        district="Chennai",
        state="Tamil Nadu",
    )
    admin_user.set_password("AdminPass2026!")
    db_session.add(admin_user)

    db_session.commit()

    # Profiles
    buyer_profile = BuyerProfile(
        user_id=buyer_user.id,
        business_name="Madurai Spices Traders",
        business_type="Wholesaler",
    )
    admin_profile = AdminProfile(
        user_id=admin_user.id,
        department="Operations",
        permissions="READ,WRITE,EXECUTE",
    )
    db_session.add_all([buyer_profile, admin_profile])
    db_session.commit()

    assert buyer_user.role == "buyer"
    assert buyer_user.buyer_profile.business_name == "Madurai Spices Traders"
    assert admin_user.role == "admin"
    assert admin_user.admin_profile.department == "Operations"


def test_audit_logs_creation(db_session):
    """
    Verify audit logging table creation and foreign key behavior
    """
    admin_user = User(
        full_name="Audit Admin",
        phone="+919876500004",
        role="admin",
    )
    admin_user.set_password("AdminPass2026!")
    db_session.add(admin_user)
    db_session.commit()

    log_entry = AuditLog(
        user_id=admin_user.id,
        action="CREATE_USER",
        entity_type="users",
        entity_id=admin_user.id,
        ip_address="127.0.0.1",
    )
    db_session.add(log_entry)
    db_session.commit()

    fetched_log = db_session.query(AuditLog).filter_by(action="CREATE_USER").first()
    assert fetched_log is not None
    assert fetched_log.user_id == admin_user.id


def test_products_schema_and_seed_sql():
    """
    Verify schema.sql and seed.sql definitions for products table, indexes, and FK constraints.
    """
    import os

    schema_path = os.path.join(os.path.dirname(__file__), "..", "database", "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    assert "CREATE TABLE IF NOT EXISTS products" in schema_sql
    assert "farmer_id INT NOT NULL" in schema_sql
    assert "name VARCHAR(150) NOT NULL" in schema_sql
    assert "category VARCHAR(100) NOT NULL" in schema_sql
    assert "quantity DECIMAL(10,2) NOT NULL" in schema_sql
    assert "unit VARCHAR(20)" in schema_sql
    assert "asking_price DECIMAL(10,2) NOT NULL" in schema_sql
    assert "status VARCHAR(50)" in schema_sql
    assert "CONSTRAINT fk_products_farmer FOREIGN KEY (farmer_id) REFERENCES users(id) ON DELETE CASCADE" in schema_sql
    assert "INDEX idx_products_farmer_id (farmer_id)" in schema_sql
    assert "INDEX idx_products_name (name)" in schema_sql
    assert "INDEX idx_products_category (category)" in schema_sql
    assert "INDEX idx_products_status (status)" in schema_sql
    assert "INDEX idx_products_created_at (created_at)" in schema_sql

    seed_path = os.path.join(os.path.dirname(__file__), "..", "database", "seed.sql")
    with open(seed_path, "r", encoding="utf-8") as f:
        seed_sql = f.read()

    assert "INSERT INTO products" in seed_sql
