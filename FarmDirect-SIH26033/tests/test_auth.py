"""
Automated Test Suite for Authentication & Role-Based Access Control (SIH26033)
"""
import pytest


def test_farmer_registration_and_login(client):
    """
    Test Farmer registration, login, profile retrieval, and dashboard access.
    """
    farmer_payload = {
        "full_name": "Ramesh Kumar",
        "phone_number": "9876543210",
        "email": "ramesh.farmer@example.com",
        "password": "FarmerPassword123",
        "role": "FARMER",
        "location": "Salem, Tamil Nadu",
        "farm_size_acres": 5.5,
        "primary_crops": "Paddy, Sugarcane",
    }

    # 1. Register Farmer
    reg_response = client.post("/api/auth/register", json=farmer_payload)
    assert reg_response.status_code == 201
    reg_data = reg_response.get_json()
    assert reg_data["status"] == "success"
    assert "token" in reg_data["data"]
    user_info = reg_data["data"]["user"]
    assert user_info["role"] == "FARMER"
    assert user_info["full_name"] == "Ramesh Kumar"
    assert user_info["profile"]["location"] == "Salem, Tamil Nadu"

    # Security check: Password and hash must NOT be in response
    assert "password" not in user_info
    assert "password_hash" not in user_info

    # 2. Login Farmer
    login_response = client.post(
        "/api/auth/login",
        json={
            "phone_number": "9876543210",
            "password": "FarmerPassword123",
            "role": "FARMER",
        },
    )
    assert login_response.status_code == 200
    login_data = login_response.get_json()
    token = login_data["data"]["token"]
    assert token is not None

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Get Farmer Profile
    profile_response = client.get("/api/auth/profile", headers=headers)
    assert profile_response.status_code == 200
    profile_data = profile_response.get_json()
    assert profile_data["data"]["user"]["phone_number"] == "9876543210"

    # 4. Access Protected Farmer Dashboard
    dashboard_response = client.get("/api/farmer/dashboard", headers=headers)
    assert dashboard_response.status_code == 200
    dashboard_data = dashboard_response.get_json()
    assert dashboard_data["status"] == "success"


def test_buyer_registration_and_rbac(client):
    """
    Test Buyer registration and RBAC enforcement (Buyer cannot access Admin routes).
    """
    buyer_payload = {
        "full_name": "Anand Traders",
        "phone_number": "9123456789",
        "email": "anand@traders.com",
        "password": "BuyerPassword123",
        "role": "BUYER",
        "business_name": "Anand Wholesale Produce",
        "business_type": "Wholesaler",
        "location": "Chennai, Tamil Nadu",
    }

    # 1. Register Buyer
    reg_response = client.post("/api/auth/register", json=buyer_payload)
    assert reg_response.status_code == 201

    # 2. Login Buyer
    login_response = client.post(
        "/api/auth/login",
        json={
            "identifier": "anand@traders.com",
            "password": "BuyerPassword123",
        },
    )
    assert login_response.status_code == 200
    token = login_response.get_json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Access Protected Buyer Dashboard (Authorized: 200)
    buyer_dash = client.get("/api/buyer/dashboard", headers=headers)
    assert buyer_dash.status_code == 200

    # 4. Access Protected Admin Metrics (Forbidden: 403)
    admin_metrics = client.get("/api/admin/metrics", headers=headers)
    assert admin_metrics.status_code == 403
    assert admin_metrics.get_json()["status"] == "error"


def test_admin_registration_and_full_access(client):
    """
    Test Admin registration, login, and full RBAC privileges.
    """
    admin_payload = {
        "full_name": "System Admin",
        "phone_number": "9000000000",
        "email": "admin@farmdirect.gov.in",
        "password": "AdminSuperSecret123",
        "role": "ADMIN",
    }

    client.post("/api/auth/register", json=admin_payload)

    login_resp = client.post(
        "/api/auth/login",
        json={
            "phone_number": "9000000000",
            "password": "AdminSuperSecret123",
        },
    )
    token = login_resp.get_json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Admin accesses Admin metrics (200)
    assert client.get("/api/admin/metrics", headers=headers).status_code == 200
    # Admin accesses Farmer dashboard (200)
    assert client.get("/api/farmer/dashboard", headers=headers).status_code == 200
    # Admin accesses Buyer dashboard (200)
    assert client.get("/api/buyer/dashboard", headers=headers).status_code == 200


def test_duplicate_user_prevention(client):
    """
    Test that registering duplicate phone numbers or emails returns 400 Bad Request.
    """
    user_payload = {
        "full_name": "Test User",
        "phone_number": "9998887770",
        "email": "dup@example.com",
        "password": "Password123",
        "role": "FARMER",
    }

    # First registration succeeds
    resp1 = client.post("/api/auth/register", json=user_payload)
    assert resp1.status_code == 201

    # Duplicate phone number fails
    dup_phone_payload = user_payload.copy()
    dup_phone_payload["email"] = "other@example.com"
    resp2 = client.post("/api/auth/register", json=dup_phone_payload)
    assert resp2.status_code == 400
    assert "phone number" in resp2.get_json()["message"].lower()

    # Duplicate email fails
    dup_email_payload = user_payload.copy()
    dup_email_payload["phone_number"] = "9998887771"
    resp3 = client.post("/api/auth/register", json=dup_email_payload)
    assert resp3.status_code == 400
    assert "email" in resp3.get_json()["message"].lower()


def test_invalid_credentials_and_validation(client):
    """
    Test validation errors for invalid inputs and authentication failures.
    """
    # 1. Missing required fields in registration
    invalid_reg = client.post("/api/auth/register", json={"full_name": "Only Name"})
    assert invalid_reg.status_code == 400
    assert invalid_reg.get_json()["status"] == "error"

    # 2. Invalid role
    bad_role = client.post(
        "/api/auth/register",
        json={
            "full_name": "Bad Role",
            "phone_number": "9888877777",
            "password": "Password123",
            "role": "SUPERUSER",
        },
    )
    assert bad_role.status_code == 400

    # 3. Wrong password during login
    # Register first
    client.post(
        "/api/auth/register",
        json={
            "full_name": "Login User",
            "phone_number": "9777766666",
            "password": "CorrectPassword123",
            "role": "BUYER",
        },
    )
    wrong_pass = client.post(
        "/api/auth/login",
        json={
            "phone_number": "9777766666",
            "password": "WrongPassword",
        },
    )
    assert wrong_pass.status_code == 401


def test_unauthenticated_requests(client):
    """
    Test that accessing protected endpoints without auth header returns 401.
    """
    # No auth header
    resp1 = client.get("/api/auth/profile")
    assert resp1.status_code == 401

    # Invalid Bearer token
    resp2 = client.get("/api/auth/profile", headers={"Authorization": "Bearer invalid_token_xyz"})
    assert resp2.status_code == 401


def test_profile_update_and_logout(client):
    """
    Test profile update endpoint and logout.
    """
    # Register & Login
    reg_resp = client.post(
        "/api/auth/register",
        json={
            "full_name": "Original Name",
            "phone_number": "9666655555",
            "password": "Password123",
            "role": "FARMER",
        },
    )
    token = reg_resp.get_json()["data"]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Update Profile
    update_resp = client.put(
        "/api/auth/profile",
        headers=headers,
        json={
            "full_name": "Updated Name",
            "location": "Coimbatore, Tamil Nadu",
            "farm_size_acres": 12.0,
        },
    )
    assert update_resp.status_code == 200
    updated_user = update_resp.get_json()["data"]["user"]
    assert updated_user["full_name"] == "Updated Name"
    assert updated_user["profile"]["location"] == "Coimbatore, Tamil Nadu"
    assert updated_user["profile"]["farm_size_acres"] == 12.0

    # Logout
    logout_resp = client.post("/api/auth/logout", headers=headers)
    assert logout_resp.status_code == 200
    assert logout_resp.get_json()["status"] == "success"
