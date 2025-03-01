from fastapi.testclient import TestClient
from api.main import app
from api.utils import find_index
from api.data import data

client = TestClient(app)


def get_expected_data(value: int) -> dict[str, int]:
    """Returns the expected response for a given value."""
    index = find_index(value, data["numbers"])
    return {"value": value, "index": index}


def test_read_index_successfuly_returns_correct_value_and_index():
    value = 100
    response = client.get(f"/index/{value}/")
    assert response.status_code == 200
    assert response.json() == get_expected_data(value)


def test_read_index_returns_404_in_case_of_missing_index():
    value = 1
    response = client.get(f"/index/{value}/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Index not found."}
