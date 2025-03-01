import pytest
from api.data import load_numbers
from api.data import data


@pytest.fixture(scope="module", autouse=True)
def setup_data():
    """Ensures data is loaded before running tests."""
    data["numbers"] = load_numbers()
