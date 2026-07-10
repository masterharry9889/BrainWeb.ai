import json
import asyncio
import os
from typing import AsyncGenerator
import redis.asyncio as aioredis

REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

async def publish_event(channel: str, event_type: str, data: dict):
    """
    Publish an event to a Redis channel.
    Event types: run.started, run.token, run.finished, run.error
    """
    payload = {
        "type": event_type,
        "data": data
    }
    await redis_client.publish(channel, json.dumps(payload))

async def subscribe_events(channel: str) -> AsyncGenerator[dict, None]:
    """
    Subscribe to a Redis channel and yield events.
    """
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)
    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                yield json.loads(message['data'])
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()

async def psubscribe_events(pattern: str) -> AsyncGenerator[dict, None]:
    """
    Subscribe to a Redis pattern and yield events.
    """
    pubsub = redis_client.pubsub()
    await pubsub.psubscribe(pattern)
    try:
        async for message in pubsub.listen():
            if message['type'] == 'pmessage':
                yield json.loads(message['data'])
    finally:
        await pubsub.punsubscribe(pattern)
        await pubsub.close()
