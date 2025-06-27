import os
import logging
from fastapi import HTTPException
from cachetools import TTLCache
from stytch import B2BClient
from stytch.core.response_base import StytchError

 # --- Environment Validation ---
STYTCH_PROJECT_ID = os.getenv("STYTCH_PROJECT_ID")
STYTCH_SECRET = os.getenv("STYTCH_SECRET")
APP_ENV = os.getenv("APP_ENV", "local")
ENVIRONMENT = "test" if APP_ENV != "production" else "live"

missing_vars = [var for var in ["STYTCH_PROJECT_ID", "STYTCH_SECRET"] if not os.getenv(var)]
if missing_vars:
    raise RuntimeError(f"Missing required env vars: {', '.join(missing_vars)}")

# --- Logger Setup ---
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- Stytch Client ---
client = B2BClient(
    project_id=STYTCH_PROJECT_ID,
    secret=STYTCH_SECRET,
    environment=ENVIRONMENT,
)

# --- In-Memory Token Cache ---
token_cache = TTLCache(maxsize=500, ttl=300)

# --- Token Verifier ---
def verify_session_token(token: str) -> dict:
    """
    Verifies a session token with Stytch and caches the result.

    Args:
        token (str): The session token.

    Returns:
        dict: Member and org data from Stytch.

    Raises:
        HTTPException: If the token is invalid or verification fails.
    """
    if token in token_cache:
        logger.info("✅ Token cache hit")
        return token_cache[token]

    logger.info("🔍 Verifying session token with Stytch")

    try:
        response = client.sessions.authenticate(session_token=token)
        token_cache[token] = response
        logger.info("✅ Token verified successfully")
        return response
    except StytchError as e:
        logger.error(f"❌ Stytch API error: {e}")
        raise HTTPException(status_code=401, detail="Invalid session token")
    except Exception as e:
        logger.error(f"❌ Unexpected auth error: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")