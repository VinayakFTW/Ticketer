import redis

from brain.config import ENVIRONMENT_VARIABLES


redis_client = redis.Redis(
    host=ENVIRONMENT_VARIABLES.get("REDIS_HOST"),
    port=ENVIRONMENT_VARIABLES.get("REDIS_PORT"),
    decode_responses=True,
    username="default",
    password=ENVIRONMENT_VARIABLES.get("REDIS_PASSWORD"),
)
