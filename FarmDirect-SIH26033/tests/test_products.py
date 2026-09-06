"""
Automated Test Suite for Product Management & Marketplace Functionality
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
import pytest
from backend.models import User, FarmerProfile, Product


def test_product_model_creation_and_to_dict(db_session):
    """
    Verify Product ORM model creation, field accuracy matching schema.sql,
    relationships, and to_dict() serialization without invalid User attributes.
    """
    farmer = User(
        full_name="Selvam Farmer",
        email="selvam@agro.com",
        phone="+919876599901",
        role="farmer",
        district="Thanjavur",
        state="Tamil Nadu",
    )
    farmer.set_password("FarmerPass2026!")
    db_session.add(farmer)
    db_session.commit()

    farmer_profile = FarmerProfile(
        user_id=farmer.id,
        farm_name="Delta Paddy Farm",
        crop_types="Paddy, Sugarcane",
        land_area=8.0,
        location="Thanjavur Rural",
        verification_status="verified",
    )
    db_session.add(farmer_profile)
    db_session.commit()

    product = Product(
        farmer_id=farmer.id,
        name="Ponni Rice Paddy",
        category="Grains",
        description="Freshly harvested organic Ponni paddy",
        quantity=1500.50,
        unit="kg",
        asking_price=45.00,
        location="Thanjavur Mandi",
        status="active",
    )
    db_session.add(product)
    db_session.commit()

    # Query product
    saved_product = db_session.query(Product).filter_by(name="Ponni Rice Paddy").first()
    assert saved_product is not None
    assert saved_product.farmer_id == farmer.id
    assert saved_product.category == "Grains"
    assert float(saved_product.quantity) == 1500.50
    assert float(saved_product.asking_price) == 45.00
    assert saved_product.unit == "kg"
    assert saved_product.status == "active"

    # Test relationship
    assert saved_product.farmer.full_name == "Selvam Farmer"
    assert len(farmer.products) == 1
    assert farmer.products[0].name == "Ponni Rice Paddy"

    # Test to_dict() output & valid User attributes
    dict_data = saved_product.to_dict()
    assert dict_data["id"] == saved_product.id
    assert dict_data["farmer_id"] == farmer.id
    assert dict_data["name"] == "Ponni Rice Paddy"
    assert dict_data["asking_price"] == 45.00
    assert "farmer" in dict_data
    assert dict_data["farmer"]["id"] == farmer.id
    assert dict_data["farmer"]["full_name"] == "Selvam Farmer"
    assert dict_data["farmer"]["phone"] == "+919876599901"
    assert dict_data["farmer"]["district"] == "Thanjavur"
    assert dict_data["farmer"]["state"] == "Tamil Nadu"
    assert dict_data["farmer"]["farm_name"] == "Delta Paddy Farm"


def test_product_user_cascade_delete(db_session):
    """
    Verify ON DELETE CASCADE behavior when farmer user is deleted.
    """
    farmer = User(
        full_name="Cascade Farmer",
        email="cascade@farmer.com",
        phone="+919876599902",
        role="farmer",
    )
    farmer.set_password("Pass2026!")
    db_session.add(farmer)
    db_session.commit()

    product = Product(
        farmer_id=farmer.id,
        name="Red Chillies",
        category="Spices",
        quantity=100.0,
        asking_price=200.0,
    )
    db_session.add(product)
    db_session.commit()

    product_id = product.id
    db_session.delete(farmer)
    db_session.commit()

    deleted_product = db_session.query(Product).filter_by(id=product_id).first()
    assert deleted_product is None


def test_product_api_crud_flow(client, db_session):
    """
    Verify API endpoints for creating, retrieving, updating, and deleting products.
    """
    farmer = User(
        full_name="API Test Farmer",
        email="apifarmer@example.com",
        phone="+919876599903",
        role="farmer",
        district="Madurai",
        state="Tamil Nadu",
    )
    farmer.set_password("FarmerPass2026!")
    db_session.add(farmer)
    db_session.commit()

    # 1. Create product via API
    payload = {
        "farmer_id": farmer.id,
        "name": "Fresh Organic Carrots",
        "category": "Vegetables",
        "description": "Sweet crunch orange carrots",
        "quantity": 250.0,
        "unit": "kg",
        "asking_price": 50.0,
        "location": "Madurai Market",
    }
    response = client.post("/api/marketplace/products", json=payload)
    assert response.status_code == 201
    res_data = response.get_json()
    assert res_data["status"] == "success"
    product_id = res_data["data"]["id"]
    assert res_data["data"]["name"] == "Fresh Organic Carrots"

    # 2. Get product by ID
    get_res = client.get(f"/api/marketplace/products/{product_id}")
    assert get_res.status_code == 200
    assert get_res.get_json()["data"]["category"] == "Vegetables"

    # 3. List products
    list_res = client.get("/api/marketplace/products?category=Vegetables")
    assert list_res.status_code == 200
    assert list_res.get_json()["count"] >= 1

    # 4. Update product
    update_payload = {"asking_price": 45.0, "status": "active"}
    put_res = client.put(f"/api/marketplace/products/{product_id}", json=update_payload)
    assert put_res.status_code == 200
    assert put_res.get_json()["data"]["asking_price"] == 45.0

    # 5. Get categories
    cat_res = client.get("/api/marketplace/categories")
    assert cat_res.status_code == 200
    assert "Vegetables" in cat_res.get_json()["data"]

    # 6. Delete product
    del_res = client.delete(f"/api/marketplace/products/{product_id}")
    assert del_res.status_code == 200

    # Verify 404 after deletion
    get_after_del = client.get(f"/api/marketplace/products/{product_id}")
    assert get_after_del.status_code == 404


def test_product_api_validation(client, db_session):
    """
    Verify error handling and input validation in marketplace API.
    """
    # Missing required fields
    response = client.post("/api/marketplace/products", json={"name": "Incomplete"})
    assert response.status_code == 400
    assert response.get_json()["status"] == "error"

    # Non-existent farmer_id
    response2 = client.post("/api/marketplace/products", json={
        "farmer_id": 99999,
        "name": "Invalid Farmer Produce",
        "category": "Grains",
        "quantity": 10.0,
        "asking_price": 10.0,
    })
    assert response2.status_code == 404

    # Negative quantity
    farmer = User(
        full_name="Valid Farmer",
        phone="+919876599904",
        role="farmer",
    )
    farmer.set_password("Pass2026!")
    db_session.add(farmer)
    db_session.commit()

    response3 = client.post("/api/marketplace/products", json={
        "farmer_id": farmer.id,
        "name": "Bad Qty Product",
        "category": "Grains",
        "quantity": -5.0,
        "asking_price": 10.0,
    })
    assert response3.status_code == 400
