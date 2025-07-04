import os
import logging
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from contextlib import asynccontextmanager
import redis.asyncio as redis
from agent import explain_like_im_five
from auth import get_current_user, get_current_org_id
from pydantic import BaseModel

ENV_FILE = os.getenv("APP_ENV", ".env.local")
load_dotenv(dotenv_path=ENV_FILE)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplainRequest(BaseModel):
    topic: str


async def get_rate_limit_key(request: Request) -> str:
    token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
    return f"ratelimit:{token}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = os.getenv("REDIS_URL")
    redis_client = redis.from_url(redis_url, encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis_client, identifier=get_rate_limit_key)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/explain", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def explain(
    request: ExplainRequest,
    user_data=Depends(get_current_user),
    org_id=Depends(get_current_org_id),
):
    logger.info(f"Received request to explain: {request.topic}")
    if not user_data:
        logger.warning("Unauthorized access attempt")
        raise HTTPException(status_code=401, detail="Unauthorized")
    logger.info("Calling agent...")
    response = await explain_like_im_five(request.topic, org_id=org_id)
    logger.info("Agent returned response")
    return {"response": response}


@app.get("/cached-topics")
async def get_cached_topics(org_id=Depends(get_current_org_id)):
    client = redis.from_url(
        os.getenv("REDIS_URL"), encoding="utf8", decode_responses=True
    )
    topics = await client.lrange(f"org:{org_id}:topics", 0, -1)
    return {"topics": topics}
