import pytest
from fastapi.testclient import TestClient

from db_connection import get_session
from main import app


@pytest.fixture
def client(session):
    app.dependency_overrides |= {
        get_session: lambda: session
    }
    testClient = TestClient(app)
    return testClient


def test_endpoint_add_basic_user(client):
    user = {
        "username": "lyampayet",
        "password": "difficultpassword",
        "email": "lyampayet@email.com",
    }

    response = client.post("/register/user", json=user)
    assert response.status_code == 201
    assert response.json() == {
        "message": "user created",
        "user": {
            "username": "lyampayet",
            "email": "lyampayet@email.com",
        },
    }
