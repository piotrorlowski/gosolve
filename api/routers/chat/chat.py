from fastapi import APIRouter
from langchain.schema import HumanMessage

from api.data import data
from api.routers.chat.schema import ChatRequest

router = APIRouter()


@router.post("/chat/")
async def chat(request: ChatRequest):
    chat = data["chat"]
    ai_message = chat.invoke(request.message)
    return {"response": ai_message.content}
