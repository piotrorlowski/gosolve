from pydantic import BaseModel


class IndexItem(BaseModel):
    value: int
    index: int
