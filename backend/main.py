import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import explain_like_im_five
from auth import verify_session_token

# Load environment variables
ENV_FILE = os.getenv("ENV_FILE", ".env.local")
load_dotenv(dotenv_path=ENV_FILE)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# CORS settings (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add prod domain here if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# Route: Explain a topic
@app.post("/explain")
def explain(request: ExplainRequest, user_data=Depends(get_current_user)):
    logger.info(f"Received request to explain: {request.topic}")
    logger.debug(f"Verified user: {user_data}")
    logger.info("Calling agent...")
    response = explain_like_im_five(request.topic)
    logger.info("Agent returned response")
    return {"response": response}
