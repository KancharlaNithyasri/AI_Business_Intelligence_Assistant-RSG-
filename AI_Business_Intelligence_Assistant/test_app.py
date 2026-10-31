from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_total_revenue():
    response = client.post(
        "/ask",
        json={"question": "What is the total revenue?"}
    )

    assert response.status_code == 200
    assert response.json()["result"]["value"] == 1439200


def test_top_product():
    response = client.post(
        "/ask",
        json={"question": "Which product generated the highest revenue?"}
    )

    assert response.status_code == 200
    assert response.json()["result"]["product"] == "Monitor"


def test_top_region():
    response = client.post(
        "/ask",
        json={"question": "Which region has the highest sales?"}
    )

    assert response.status_code == 200
    assert response.json()["result"]["region"] == "South"


def test_month_comparison():
    response = client.post(
        "/ask",
        json={"question": "Compare January and February revenue"}
    )

    assert response.status_code == 200
    assert response.json()["result"]["difference"] == 24350


def test_unsupported_question():
    response = client.post(
        "/ask",
        json={"question": "Tell me a joke"}
    )

    assert response.status_code == 200
    assert "error" in response.json()["result"]