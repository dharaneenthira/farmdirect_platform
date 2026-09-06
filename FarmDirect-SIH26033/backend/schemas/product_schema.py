"""
Product Schema Validation Module
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""


def validate_product_data(data, is_update=False):
    """
    Validates product payload for creation and update requests.
    Returns (errors_dict, cleaned_data_dict).
    """
    errors = {}
    cleaned = {}

    if not isinstance(data, dict):
        return {"_error": "Invalid JSON payload format."}, {}

    # farmer_id
    if "farmer_id" in data:
        try:
            cleaned["farmer_id"] = int(data["farmer_id"])
        except (ValueError, TypeError):
            errors["farmer_id"] = "farmer_id must be a valid integer."
    elif not is_update:
        errors["farmer_id"] = "farmer_id is required."

    # name
    if "name" in data:
        name = str(data["name"]).strip()
        if not name or len(name) > 150:
            errors["name"] = "Name must be non-empty and up to 150 characters."
        else:
            cleaned["name"] = name
    elif not is_update:
        errors["name"] = "name is required."

    # category
    if "category" in data:
        category = str(data["category"]).strip()
        if not category or len(category) > 100:
            errors["category"] = "Category must be non-empty and up to 100 characters."
        else:
            cleaned["category"] = category
    elif not is_update:
        errors["category"] = "category is required."

    # quantity
    if "quantity" in data:
        try:
            qty = float(data["quantity"])
            if qty <= 0:
                errors["quantity"] = "Quantity must be greater than 0."
            else:
                cleaned["quantity"] = qty
        except (ValueError, TypeError):
            errors["quantity"] = "Quantity must be a valid number."
    elif not is_update:
        errors["quantity"] = "quantity is required."

    # asking_price
    if "asking_price" in data:
        try:
            price = float(data["asking_price"])
            if price < 0:
                errors["asking_price"] = "Asking price cannot be negative."
            else:
                cleaned["asking_price"] = price
        except (ValueError, TypeError):
            errors["asking_price"] = "Asking price must be a valid number."
    elif not is_update:
        errors["asking_price"] = "asking_price is required."

    # unit
    if "unit" in data and data["unit"] is not None:
        unit = str(data["unit"]).strip()
        if len(unit) > 20:
            errors["unit"] = "Unit must be up to 20 characters."
        else:
            cleaned["unit"] = unit
    elif not is_update:
        cleaned["unit"] = "kg"

    # description
    if "description" in data:
        cleaned["description"] = str(data["description"]).strip() if data["description"] else None

    # location
    if "location" in data:
        loc = str(data["location"]).strip() if data["location"] else None
        if loc and len(loc) > 255:
            errors["location"] = "Location must be up to 255 characters."
        else:
            cleaned["location"] = loc

    # status
    if "status" in data and data["status"] is not None:
        status = str(data["status"]).strip().lower()
        allowed = ("active", "inactive", "sold_out")
        if status not in allowed:
            errors["status"] = f"Status must be one of: {', '.join(allowed)}."
        else:
            cleaned["status"] = status
    elif not is_update:
        cleaned["status"] = "active"

    return errors, cleaned
