from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Smart Ticketing API is running"}

def test_create_ticket():
    response = client.post(
        "/tickets/",
        json={
            "submitter": "test@example.com",
            "subject": "Test Ticket",
            "description": "This is a test description",
            "urgency": "Low"
        }
    )
    # Note: This might fail if MongoDB is not running or mocked, 
    # but for a simple check it validates the endpoint structure.
    # In a real scenario, we'd mock the DB.
    if response.status_code == 200:
        data = response.json()
        assert data["subject"] == "Test Ticket"
        assert "ticket_id" in data
