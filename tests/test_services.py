import pytest

from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


def test_get_word(test_client: TestClient):
    response = test_client.get("/word/challenge", params={"translated_language": "pt"})
    assert response.status_code == 200
    assert response.json()["word"] == "challenge"
