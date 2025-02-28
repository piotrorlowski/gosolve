import os
import logging

from dotenv import load_dotenv
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import index
from app.data import data
from app.data import load_numbers

load_dotenv()

port = int(os.getenv("PORT", 8000))
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Loads data when FastAPI starts."""
    data["numbers"] = load_numbers()
    logger.info(f"Data loaded successfully with {len(data['numbers'])} numbers.")
    yield
    data.clear()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(index.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
