import os
import sys

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from main import app
from fastapi.encoders import jsonable_encoder

client = TestClient(app)


@pytest.fixture
def sample_event():
    return {
        "event_id": "event1",
        "coefficient": Decimal("1.5"),
        "deadline": (datetime.now() + timedelta(days=1)).isoformat(),
        "state": "NEW",
    }


def test_create_event(sample_event):
    """Test creating an event"""
    response = client.post("/event", json=jsonable_encoder(sample_event))
    assert response.status_code == 200
    data = response.json()
    assert data["event_id"] == "event1"
    assert data["state"] == "NEW"
    assert data["coefficient"] == "1.5"
    response = client.post("/event", json=jsonable_encoder(sample_event))
    assert response.status_code == 400


def test_get_event(sample_event):
    """Test getting an event by ID"""
    client.post("/event", json=jsonable_encoder(sample_event))
    response = client.get(f"/event/{sample_event['event_id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["event_id"] == sample_event["event_id"]
    assert data["state"] == sample_event["state"]
    response = client.get("/event/bad_id}")
    assert response.status_code == 404


def test_get_events(sample_event):
    """Test getting all active events"""
    client.post("/event", json=jsonable_encoder(sample_event))

    response = client.get("/events")
    assert response.status_code == 200
    events = response.json()
    assert len(events) > 0
    assert events[0]["event_id"] == sample_event["event_id"]


def test_update_coefficient(sample_event):
    """Test updating the coefficient of an event"""
    client.post("/event", json=jsonable_encoder(sample_event))
    new_coefficient = 2.0
    response = client.put(
        f"/update_coefficient?event_id={sample_event['event_id']}&new_coefficient={new_coefficient}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["coefficient"] == str(new_coefficient)

    response = client.put(f"/update_coefficient?event_id=bad_id&new_coefficient={new_coefficient}")
    assert response.status_code == 404


def test_update_status(sample_event):
    """Test updating the status of an event"""
    client.post("/event", json=jsonable_encoder(sample_event))
    new_status = "FINISHED_WIN"
    response = client.put(
        f"/update_status?event_id={sample_event['event_id']}&new_status={new_status}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["state"] == new_status
    response = client.put(f"/update_status?event_id=bad_id&new_status={new_status}")
    assert response.status_code == 404


def test_update_deadline(sample_event):
    """Test updating the deadline of an event"""
    client.post("/event", json=jsonable_encoder(sample_event))
    new_deadline = (datetime.now() + timedelta(days=2)).isoformat()
    response = client.put(
        f"/update_deadline?event_id={sample_event['event_id']}&new_deadline={new_deadline}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["deadline"] == new_deadline
    response = client.put(
        f"/update_deadline?event_id=bad_id&new_deadline={new_deadline}"
    )
    assert response.status_code == 404

