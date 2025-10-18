from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_events():
    response = client.get("/api/v1/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_event():
    data = {
        "title": "Test Event",
        "description": "Test Description",
        "latitude": 50.4501,
        "longitude": 30.5234
    }
    response = client.post("/api/v1/events/", json=data, params={"creator_id": 1})
    assert response.status_code == 200
    event = response.json()
    assert event["title"] == "Test Event"
    assert event["creator_id"] == 1

def test_get_event():
    # First create an event
    data = {
        "title": "Test Event 2",
        "description": "Test Description",
        "latitude": 50.4501,
        "longitude": 30.5234
    }
    create_response = client.post("/api/v1/events/", json=data, params={"creator_id": 1})
    event_id = create_response.json()["id"]

    # Then get it
    response = client.get(f"/api/v1/events/{event_id}")
    assert response.status_code == 200
    event = response.json()
    assert event["id"] == event_id

def test_update_event():
    # Create
    data = {
        "title": "Test Event 3",
        "description": "Test Description",
        "latitude": 50.4501,
        "longitude": 30.5234
    }
    create_response = client.post("/api/v1/events/", json=data, params={"creator_id": 1})
    event_id = create_response.json()["id"]

    # Update
    update_data = {
        "title": "Updated Event",
        "description": "Updated Description",
        "latitude": 50.4501,
        "longitude": 30.5234
    }
    response = client.put(f"/api/v1/events/{event_id}", json=update_data)
    assert response.status_code == 200
    event = response.json()
    assert event["title"] == "Updated Event"

def test_delete_event():
    # Create
    data = {
        "title": "Test Event 4",
        "description": "Test Description",
        "latitude": 50.4501,
        "longitude": 30.5234
    }
    create_response = client.post("/api/v1/events/", json=data, params={"creator_id": 1})
    event_id = create_response.json()["id"]

    # Delete
    response = client.delete(f"/api/v1/events/{event_id}")
    assert response.status_code == 200

    # Check it's gone
    get_response = client.get(f"/api/v1/events/{event_id}")
    assert get_response.status_code == 404

def test_create_user():
    data = {
        "telegram_id": 12345,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post("/api/v1/users/", json=data)
    assert response.status_code == 200
    user = response.json()
    assert user["telegram_id"] == 12345