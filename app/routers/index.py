from fastapi import APIRouter
from typing import Union

from app.utils import find_index
from app.data import data

router = APIRouter()


@router.get("/index/{value}/", tags=["users"])
async def read_index(value: int) -> dict[str, Union[int, str]]:
    """Returns the index of the value in the list."""
    result = find_index(value, data["numbers"])
    if result is None:
        return {"error_message": "Index not found."}
    return {"value": value, "index": result}
