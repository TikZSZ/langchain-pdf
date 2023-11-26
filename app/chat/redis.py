import os
from redis import Redis

client = Redis.from_url(
  os.getenv("REDIS_URI"),
  decode_responses=True
)