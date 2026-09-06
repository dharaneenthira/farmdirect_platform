"""
Marketplace & Product Management Routes
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
from flask import Blueprint, request, jsonify
from backend.db.session import db_session
from backend.models import Product, User
from backend.schemas.product_schema import validate_product_data

marketplace_bp = Blueprint("marketplace", __name__)


@marketplace_bp.route("/products", methods=["GET"])
def get_products():
    """
    Retrieve product listings with optional query filtering and pagination.
    Query params: category, status, farmer_id, search/q, page, per_page
    """
    category = request.args.get("category", type=str)
    status = request.args.get("status", type=str)
    farmer_id = request.args.get("farmer_id", type=int)
    search_query = request.args.get("q", request.args.get("search", type=str), type=str)

    query = db_session.query(Product)

    if category:
        query = query.filter(Product.category.ilike(f"%{category.strip()}%"))
    if status:
        query = query.filter(Product.status == status.strip())
    if farmer_id:
        query = query.filter(Product.farmer_id == farmer_id)
    if search_query:
        term = f"%{search_query.strip()}%"
        query = query.filter(
            (Product.name.ilike(term)) | (Product.description.ilike(term))
        )

    products = query.order_by(Product.created_at.desc()).all()
    return jsonify({
        "status": "success",
        "count": len(products),
        "data": [p.to_dict() for p in products]
    }), 200


@marketplace_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    """
    Retrieve details of a single product by ID.
    """
    product = db_session.query(Product).filter_by(id=product_id).first()
    if not product:
        return jsonify({
            "status": "error",
            "message": f"Product with ID {product_id} not found."
        }), 404

    return jsonify({
        "status": "success",
        "data": product.to_dict()
    }), 200


@marketplace_bp.route("/products", methods=["POST"])
def create_product():
    """
    Create a new product listing.
    """
    data = request.get_json(silent=True) or {}
    errors, cleaned = validate_product_data(data, is_update=False)

    if errors:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "errors": errors
        }), 400

    # Verify farmer user exists
    farmer = db_session.query(User).filter_by(id=cleaned["farmer_id"]).first()
    if not farmer:
        return jsonify({
            "status": "error",
            "message": f"Farmer user with ID {cleaned['farmer_id']} does not exist."
        }), 404

    product = Product(
        farmer_id=cleaned["farmer_id"],
        name=cleaned["name"],
        category=cleaned["category"],
        description=cleaned.get("description"),
        quantity=cleaned["quantity"],
        unit=cleaned.get("unit", "kg"),
        asking_price=cleaned["asking_price"],
        location=cleaned.get("location"),
        status=cleaned.get("status", "active"),
    )

    db_session.add(product)
    db_session.commit()

    return jsonify({
        "status": "success",
        "message": "Product created successfully",
        "data": product.to_dict()
    }), 201


@marketplace_bp.route("/products/<int:product_id>", methods=["PUT", "PATCH"])
def update_product(product_id):
    """
    Update an existing product listing.
    """
    product = db_session.query(Product).filter_by(id=product_id).first()
    if not product:
        return jsonify({
            "status": "error",
            "message": f"Product with ID {product_id} not found."
        }), 404

    data = request.get_json(silent=True) or {}
    errors, cleaned = validate_product_data(data, is_update=True)

    if errors:
        return jsonify({
            "status": "error",
            "message": "Validation failed",
            "errors": errors
        }), 400

    if "farmer_id" in cleaned:
        farmer = db_session.query(User).filter_by(id=cleaned["farmer_id"]).first()
        if not farmer:
            return jsonify({
                "status": "error",
                "message": f"Farmer user with ID {cleaned['farmer_id']} does not exist."
            }), 404
        product.farmer_id = cleaned["farmer_id"]

    for field in ("name", "category", "description", "quantity", "unit", "asking_price", "location", "status"):
        if field in cleaned:
            setattr(product, field, cleaned[field])

    db_session.commit()

    return jsonify({
        "status": "success",
        "message": "Product updated successfully",
        "data": product.to_dict()
    }), 200


@marketplace_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a product listing by ID.
    """
    product = db_session.query(Product).filter_by(id=product_id).first()
    if not product:
        return jsonify({
            "status": "error",
            "message": f"Product with ID {product_id} not found."
        }), 404

    db_session.delete(product)
    db_session.commit()

    return jsonify({
        "status": "success",
        "message": "Product deleted successfully"
    }), 200


@marketplace_bp.route("/categories", methods=["GET"])
def get_categories():
    """
    Get distinct product categories available in the marketplace.
    """
    categories = (
        db_session.query(Product.category)
        .distinct()
        .order_by(Product.category.asc())
        .all()
    )
    cat_list = [c[0] for c in categories if c[0]]
    return jsonify({
        "status": "success",
        "data": cat_list
    }), 200
