from contextlib import asynccontextmanager

from typing import Union

from fastapi import FastAPI
import numpy as np

data = {}


def load_numbers():
    """Reads the numbers from the file and loads them into a list."""
    return np.loadtxt("input.txt", dtype=int).tolist()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Loads the numbers when FastAPI starts."""
    data["numbers"] = load_numbers()
    yield
    data.clear()


app = FastAPI(lifespan=lifespan)


def find_index(value: int) -> Union[int, None]:
    """Finds the index of the value in the list."""
    numbers = data["numbers"]

    if value in numbers:
        return numbers.index(value)

    lower_bound = value * (1 - 0.1)
    upper_bound = value * (1 + 0.1)

    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] < value:
            left = mid + 1
        else:
            right = mid - 1

    candidates = []
    if right >= 0 and numbers[right] >= lower_bound:
        candidates.append(numbers[right])
    if left < len(numbers) and numbers[left] <= upper_bound:
        candidates.append(numbers[left])

    if candidates:
        closest_value = min(candidates, key=lambda x: abs(x - value))
        return numbers.index(closest_value)

    return None


@app.get("/items/{value}")
async def get_(value: int, q: Union[str, None] = None) -> dict:
    result = find_index(value)
    if result is None:
        return {"error_message": "Item not found."}
    return {"value": value, "index": result}
