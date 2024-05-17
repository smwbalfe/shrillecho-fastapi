import redis
from core import config

print(f"connecting to redis: {config.redis_origin}:6379")
r = redis.Redis(host=config.redis_origin, port=6379, db=0, decode_responses=True)