import re
import html
import redis.asyncio as redis
import os


async def redis_client() -> redis.Redis:
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        return redis.from_url(redis_url, encoding="utf8", decode_responses=True)
    raise ValueError("REDIS_URL environment variable is not set.")


async def store_topic_in_cache(topic: str) -> None:
    """
    Stores a topic in the Redis cache for an organization.

    Args:
        topic (str): The topic to store.
        org_id (str): The organization ID to associate with the topic.
    """
    if not topic:
        return

    client = redis_client()
    cache_key = f"org:topics"
    # Use a list to store the last 5 topics
    client.lpush(cache_key, topic)
    # Trim the list to the last 5 topics
    client.ltrim(cache_key, 0, 4)
    # Optionally set an expiration time for the list (e.g., 1 week)
    client.expire(cache_key, 604800)


async def get_cached_topics() -> list:
    """
    Retrieves the cached topics for an organization.

    Returns:
        list: A list of topics stored in the cache.
    """
    client = redis_client()
    cache_key = f"org:topics"
    topics = client.lrange(cache_key, 0, -1)
    return topics if topics else []


def sanitize_string(text: str) -> str:
    """
    Cleans a string by escaping HTML and removing control characters.

    Args:
        text (str): The input string to sanitize.

    Returns:
        str: The sanitized string.
    """
    if not isinstance(text, str):
        return ""

    # Remove control characters and other suspicious invisible chars
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)

    # Optionally, trim long whitespace or weird characters
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
