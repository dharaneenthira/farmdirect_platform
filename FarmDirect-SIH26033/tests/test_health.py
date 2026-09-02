"""
Automated Test Suite for Backend Health Endpoint
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""


def test_health_endpoint(client):
    """
    Test GET /api/health returns 200 OK and valid JSON format
    with status, backend, and database connectivity.
    """
    response = client.get("/api/health")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "success"
    assert data["backend"] == "running"
    assert data["database"] == "connected"
