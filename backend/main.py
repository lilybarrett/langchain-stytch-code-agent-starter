import os
import logging
from dotenv import load_dotenv

from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from contextlib import asynccontextmanager
import redis.asyncio as redis
from agent import explain_like_im_five
from auth import verify_session_token
from pydantic import BaseModel

ENV_FILE = os.getenv("ENV_FILE", ".env.local")
load_dotenv(dotenv_path=ENV_FILE)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplainRequest(BaseModel):
    topic: str


def get_current_user(authorization: str = Header(...), auth_check=None):
    token = authorization.removeprefix("Bearer ").strip()
    try:
        user_data = verify_session_token(token, auth_check)
        return user_data
    except Exception as e:
        logger.error(f"Auth failed: {e}")
        raise HTTPException(status_code=401, detail="Auth error")


def get_current_org_id(authorization: str = Header(...)):
    token = authorization.removeprefix("Bearer ").strip()
    logger.debug(f"Extracted token for current_org_id: {token}")
    try:
        user_data = verify_session_token(token)
        if not user_data or not user_data.organization:
            logger.error("User data or organization not found in session")
            raise HTTPException(status_code=401, detail="Auth error")
        return user_data.organization.organization_id
    except Exception as e:
        logger.error(f"Auth failed: {e}")
        raise HTTPException(status_code=401, detail="Auth error")


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
async def explain(request: ExplainRequest, user_data=Depends(get_current_user)):
    logger.info(f"Received request to explain: {request.topic}")
    if not user_data:
        logger.warning("Unauthorized access attempt")
        raise HTTPException(status_code=401, detail="Unauthorized")
    logger.info("Calling agent...")
    response = await explain_like_im_five(request.topic)
    logger.info("Agent returned response")
    return {"response": response}


@app.get("/cached-topics")
async def get_cached_topics(org_id=Depends(get_current_org_id)):
    logger.info(f"Fetching cached topics for org_id: {org_id}")
    client = redis.from_url(
        os.getenv("REDIS_URL"), encoding="utf8", decode_responses=True
    )
    topics = await client.lrange("org:topics", 0, -1)
    if not topics:
        raise HTTPException(status_code=404, detail="No cached topics found")
    return {"topics": topics}
