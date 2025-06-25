import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine and load environment-specific .env file
app_env = os.getenv("APP_ENV", "local")
env_file = f".env.{app_env}"
env_path = os.path.join(os.path.dirname(__file__), env_file)
load_dotenv(dotenv_path=env_path)

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    timeout=20,
)


def explain_like_im_five(topic: str) -> str:
    """
    Generates a simple explanation for the given topic using an LLM.

    Args:
        topic (str): The topic to explain.

    Returns:
        str: A simplified explanation of the topic.
    """
    prompt = f"Explain this to me like I'm 5: {topic}"
    try:
        logger.info(f"Prompting LLM with: {prompt}")
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        logger.error("❌ OpenAI error: %s", e)
        return "Sorry, I'm out of brain juice right now! Try again later."
