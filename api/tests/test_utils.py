import pytest

from api.data import data
from api.utils import find_index


@pytest.fixture
def expected_values() -> list[tuple[int, int]]:
    return [
        (0, 0),
        (100, 1),
        (1100, 11),
        (1140, 11),
        (1150, 12),
        (1160, 12),
        (1000000, 10000),
        (9999900, 99999),
        (10000000, 100000),
        (10000000000000000000000000, None),
    ]


def test_find_index_returns_expected_index(expected_values):
    for value, index in expected_values:
        assert {"value": value, "index": find_index(value, data["numbers"])} == {
            "value": value,
            "index": index,
        }
