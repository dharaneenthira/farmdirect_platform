# FarmDirect API Specification

## Conventions
- **Base URL:** `/api`
- **Content Type:** `application/json`
- **Authentication:** Bearer token (`Authorization: Bearer <jwt_token>`)
- **Standard Response Format:**
```json
{
  "status": "success | error",
  "message": "Human readable description",
  "data": {}
}
```

---

## Implemented Endpoints

### 1. Health Check
- **Endpoint:** `GET /api/health`
- **Description:** Verifies backend server health.
- **Authentication:** None
- **Response `200 OK`:**
```json
{
  "status": "success",
  "message": "FarmDirect backend is running"
}
```

---

### 2. User Registration
- **Endpoint:** `POST /api/auth/register`
- **Description:** Registers a new user account (FARMER, BUYER, or ADMIN) with encrypted Werkzeug password hashing.
- **Authentication:** None
- **Request Body:**
```json
{
  "full_name": "Ramesh Kumar",
  "phone_number": "9876543210",
  "email": "ramesh@example.com",
  "password": "SecurePassword123",
  "role": "FARMER",
  "location": "Salem, Tamil Nadu",
  "farm_size_acres": 5.5,
  "primary_crops": "Paddy, Sugarcane"
}
```
- **Response `201 Created`:**
```json
{
  "status": "success",
  "message": "Farmer registered successfully",
  "data": {
    "token": "<jwt_token>",
    "user": {
      "id": 1,
      "full_name": "Ramesh Kumar",
      "phone_number": "9876543210",
      "email": "ramesh@example.com",
      "role": "FARMER",
      "is_verified": false,
      "profile": {
        "id": 1,
        "user_id": 1,
        "location": "Salem, Tamil Nadu",
        "farm_size_acres": 5.5,
        "primary_crops": "Paddy, Sugarcane"
      }
    }
  }
}
```

---

### 3. User Login
- **Endpoint:** `POST /api/auth/login`
- **Description:** Authenticates user by phone number or email and password.
- **Authentication:** None
- **Request Body:**
```json
{
  "identifier": "9876543210",
  "password": "SecurePassword123",
  "role": "FARMER"
}
```
- **Response `200 OK`:**
```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "token": "<jwt_token>",
    "user": {
      "id": 1,
      "full_name": "Ramesh Kumar",
      "phone_number": "9876543210",
      "role": "FARMER"
    }
  }
}
```

---

### 4. Get Authenticated User Profile
- **Endpoint:** `GET /api/auth/profile` or `GET /api/auth/me`
- **Description:** Returns profile details of the current authenticated user.
- **Authentication:** Bearer token required
- **Response `200 OK`:**
```json
{
  "status": "success",
  "message": "User profile retrieved successfully",
  "data": {
    "user": {
      "id": 1,
      "full_name": "Ramesh Kumar",
      "phone_number": "9876543210",
      "role": "FARMER",
      "profile": { ... }
    }
  }
}
```

---

### 5. Update Profile
- **Endpoint:** `PUT /api/auth/profile`
- **Description:** Updates authenticated user profile and role details.
- **Authentication:** Bearer token required
- **Request Body:**
```json
{
  "full_name": "Ramesh K.",
  "location": "Coimbatore, Tamil Nadu",
  "farm_size_acres": 7.0
}
```
- **Response `200 OK`:**
```json
{
  "status": "success",
  "message": "Profile updated successfully",
  "data": { "user": { ... } }
}
```

---

### 6. User Logout
- **Endpoint:** `POST /api/auth/logout`
- **Description:** Invalidates local session state.
- **Authentication:** Optional
- **Response `200 OK`:**
```json
{
  "status": "success",
  "message": "Logout successful"
}
```

---

### 7. Protected Role Routes
- **`GET /api/farmer/dashboard`**: Protected for `FARMER` and `ADMIN` roles.
- **`GET /api/buyer/dashboard`**: Protected for `BUYER` and `ADMIN` roles.
- **`GET /api/admin/metrics`**: Protected strictly for `ADMIN` role.

---

## Planned Future Endpoints
- **Farmer Services:** `GET /api/farmer/crops`, `POST /api/farmer/crops`
- **Buyer Marketplace:** `GET /api/marketplace/products`, `GET /api/marketplace/products/:id`
- **AI Services:** `POST /api/ai/predict-price`, `POST /api/ai/forecast-demand`, `POST /api/ai/match`
- **Orders:** `POST /api/orders`, `GET /api/orders/:id`, `PATCH /api/orders/:id/status`
