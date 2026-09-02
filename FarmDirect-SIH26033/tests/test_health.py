"""
Automated Test Suite for Backend Health Endpoint
"""


def test_health_endpoint(client):
    """
    Test GET /api/health returns 200 OK and status success
    """
    response = client.get("/api/health")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "success"
    assert data["message"] == "FarmDirect backend is running"
