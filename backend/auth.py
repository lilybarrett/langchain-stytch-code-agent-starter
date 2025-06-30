import os
import logging
from fastapi import HTTPException
from cachetools import TTLCache
from stytch import B2BClient
from stytch.core.response_base import StytchError

STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")
STYTCH_SECRET = os.getenv("STYTCH_SECRET")
APP_ENV = os.getenv("APP_ENV", "local")
ENVIRONMENT = "test" if APP_ENV != "production" else "live"

missing_vars = [
    var for var in ["STYTCH_PROJECT_ID", "STYTCH_SECRET"] if not os.getenv(var)
]
if missing_vars:
    raise RuntimeError(f"Missing required env vars: {', '.join(missing_vars)}")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = B2BClient(
    project_id=STYTCH_PROJECT_ID,
    secret=STYTCH_SECRET,
    environment=ENVIRONMENT,
)

token_cache = TTLCache(maxsize=500, ttl=300)


def verify_session_token(token: str, auth_check=None) -> dict:
    options = {}

    if token in token_cache:
        return token_cache[token]

    options["session_token"] = token
    if auth_check:
        options["auth_check"] = auth_check

    try:
        response = client.sessions.authenticate(**options)
        token_cache[token] = response
        return response
    except StytchError as e:
        logger.error(f"❌ Stytch API error: {e}")
        raise HTTPException(status_code=401, detail="Invalid session token")
    except Exception as e:
        logger.error(f"❌ Unexpected auth error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")
