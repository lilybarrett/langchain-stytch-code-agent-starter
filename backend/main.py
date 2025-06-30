import os
import logging
from dotenv import load_dotenv

from fastapi import FastAPI, Header, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

from pydantic import BaseModel
from contextlib import asynccontextmanager
import redis.asyncio as redis
from agent import explain_like_im_five
from auth import verify_session_token

# Load environment variables
ENV_FILE = os.getenv("ENV_FILE", ".env.local")
load_dotenv(dotenv_path=ENV_FILE)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic model for request body
class ExplainRequest(BaseModel):
    topic: str


# Dependency to extract and verify auth token
def get_current_user(authorization: str = Header(...)):
    token = authorization.removeprefix("Bearer ").strip()
    try:
        user_data = verify_session_token(token)
        return user_data
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


# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

# CORS settings (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Route: Explain a topic
@app.post("/explain", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def explain(request: ExplainRequest, user_data=Depends(get_current_user)):
    logger.info(f"Received request to explain: {request.topic}")
    logger.debug(f"Verified user: {user_data}")
    logger.info("Calling agent...")
    response = await explain_like_im_five(request.topic)
    logger.info("Agent returned response")
    return {"response": response}


# Get cached topics
@app.get("/cached-topics")
async def get_cached_topics():
    logger.info("Fetching cached topics")
    # print for debugging
    logger.debug("Connecting to Redis")
    client = redis.from_url(
        os.getenv("REDIS_URL"), encoding="utf8", decode_responses=True
    )
    topics = await client.lrange("org:topics", 0, -1)
    print(topics)
    if not topics:
        raise HTTPException(status_code=404, detail="No cached topics found")
    return {"topics": topics}
