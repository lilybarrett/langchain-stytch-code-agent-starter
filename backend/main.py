import os
import logging
from dotenv import load_dotenv

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

# Load environment variables
ENV_FILE = os.getenv("ENV_FILE", ".env.local")
load_dotenv(dotenv_path=ENV_FILE)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic model for request body
class ExplainRequest(BaseModel):
    topic: str


# Initialize FastAPI app
app = FastAPI()

# CORS settings (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Route: Explain a topic
@app.post("/explain")
async def explain(request: ExplainRequest):
    logger.info(f"Received request to explain: {request.topic}")
    response = "Explain Like I'm Five Placeholder Response!"
    logger.info("Agent returned response")
    return {"response": response}
