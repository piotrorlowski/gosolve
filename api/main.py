import os
import logging

from dotenv import load_dotenv
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import index
from api.data import data
from api.data import load_numbers

load_dotenv()

LOG_LEVEL = {
    "Info": "INFO",
    "Debug": "DEBUG",
    "Warning": "WARNING",
}

port = int(os.getenv("PORT", 8000))

log_level = LOG_LEVEL.get(os.getenv("LOG_LEVEL"))

# Fallback to a default value could be added anyway
# in case of missing .env file
# or missing variables in .env file.

if not log_level:
    raise RuntimeError("LOG_LEVEL is not set in .env file.")


logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)  # timestamp - logger name - log level - message
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Loads numbers from file into data object when FastAPI starts.

    Problems:
    - FastAPI can run in multi-worker environment.
    - Data loaded into memory won't be shared between workers.
    - Big data can also bloat memory of each worker, increasing overall
    memory consumption.

    Solution:
    - In case of the bigger data / multiple workers,
    use database instead of storing data inside memory.
    """
    try:
        data["numbers"] = load_numbers()
        logger.info(f"Data loaded successfully with {len(data['numbers'])} numbers.")
    except Exception as e:
        logger.error(f"Failed to load data: {e}")

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
