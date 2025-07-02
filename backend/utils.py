import re
import redis.asyncio as redis
import os


def redis_client() -> redis.Redis:
    redis_url = os.getenv("REDIS_URL")
    if redis_url:
        return redis.from_url(redis_url, encoding="utf8", decode_responses=True)
    raise ValueError("REDIS_URL environment variable is not set.")


async def store_topic_in_cache(topic: str, org_id: str) -> None:
    if not topic:
        return

    client = redis_client()
    cache_key = f"org:{org_id}:topics"
    # Use a list to store the last 5 topics
    await client.lpush(cache_key, topic)
    await client.ltrim(cache_key, 0, 4)
    await client.expire(cache_key, 604800)


def get_cached_topics(org_id: str) -> list:
    client = redis_client()
    cache_key = f"org:{org_id}:topics"
    topics = client.lrange(cache_key, 0, -1)
    return topics if topics else []


def sanitize_string(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Remove control characters and other suspicious invisible chars
    cleaned = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", text)

    # Optionally, trim long whitespace or weird characters
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned
