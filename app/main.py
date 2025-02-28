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

LOG_LEVEL = {
    "Info": "INFO",
    "Debug": "DEBUG",
    "Warning": "WARNING",
}

port = int(os.getenv("PORT", 8000))

log_level = LOG_LEVEL.get(os.getenv("LOG_LEVEL"))

# Fallback could be added anyway

if not log_level:
    raise RuntimeError("LOG_LEVEL is not set in .env file.")


logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Loads numbers into data when FastAPI starts.

    Problems:
    - FastAPI runs in multi-worker environment.
    - Data loaded into memory won't be shared between workers.
    - Big data can also bloat memory of each worker, increasing overall
    memory consumption.

    Solution:
    - In case of bigger data, it would be better to use database
    instead of storing data inside memory.
    """
    data["numbers"] = load_numbers()
    logger.info(f"Data loaded successfully with {len(data['numbers'])} numbers.")
    yield
    data.clear()


app = FastAPI(lifespan=lifespan)

# middleware to allow request from frontend working on a specific port

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
