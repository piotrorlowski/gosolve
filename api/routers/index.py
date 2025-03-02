from fastapi import APIRouter, HTTPException

from api.data import data
from api.routers.schema import IndexItem
from api.utils import find_index

router = APIRouter()


@router.get("/index/{value}/", response_model=IndexItem)
async def read_index(value: int) -> IndexItem:
    """Returns the index of the value in the list."""
    index = find_index(value, data["numbers"])
    if index is None:
        raise HTTPException(status_code=404, detail="Index not found.")
    return IndexItem(value=value, index=index)
