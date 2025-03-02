import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.data import data, load_numbers
from api.routers import index

load_dotenv()

API_PORT = int(os.getenv("API_PORT", 8000))
FE_PORT = int(os.getenv("FE_PORT", 5173))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)  # timestamp - logger name - log level - message
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Loads numbers from file when FastAPI starts.

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
    allow_origins=[f"http://localhost:{FE_PORT}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(index.router)

if __name__ == "__main__":
    uvicorn.run(app, port=API_PORT)
