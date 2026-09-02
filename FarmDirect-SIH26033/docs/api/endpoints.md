# FarmDirect API Specification

## Conventions
- **Base URL:** `/api`
- **Content Type:** `application/json`
- **Response Format:**
```json
{
  "status": "success | error",
  "message": "Human readable description",
  "data": {}
}
```

## Implemented Endpoints (Step 1 Foundation)

### 1. Health Check
- **Endpoint:** `GET /api/health`
- **Description:** Verifies that the Flask backend server is operational.
- **Authentication:** None
- **Response `200 OK`:**
```json
{
  "status": "success",
  "message": "FarmDirect backend is running"
}
```

## Planned Future Endpoints
- **Authentication:** `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`
- **Farmer Services:** `GET /api/farmer/crops`, `POST /api/farmer/crops`
- **Buyer Marketplace:** `GET /api/marketplace/products`, `GET /api/marketplace/products/:id`
- **AI Services:** `POST /api/ai/predict-price`, `POST /api/ai/forecast-demand`, `POST /api/ai/match`
- **Orders:** `POST /api/orders`, `GET /api/orders/:id`, `PATCH /api/orders/:id/status`
- **Admin:** `GET /api/admin/metrics`, `GET /api/admin/anomalies`
