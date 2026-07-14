import json
import asyncio
from typing import AsyncGenerator
import fnmatch

class InMemoryPubSub:
    def __init__(self):
        self.subscribers = {}
        self.psubscribers = {}
        self.history = {}

    async def publish(self, channel: str, message: str):
        if channel not in self.history:
            self.history[channel] = []
        self.history[channel].append(message)
        
        # Exact channel match
        if channel in self.subscribers:
            for queue in self.subscribers[channel]:
                await queue.put({"type": "message", "channel": channel, "data": message})
        
        # Pattern match
        for pattern, queues in self.psubscribers.items():
            if fnmatch.fnmatch(channel, pattern):
                for queue in queues:
                    await queue.put({"type": "pmessage", "pattern": pattern, "channel": channel, "data": message})

    def subscribe(self, channel: str) -> asyncio.Queue:
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        q = asyncio.Queue()
        self.subscribers[channel].append(q)
        
        if channel in self.history:
            for msg in self.history[channel]:
                q.put_nowait({"type": "message", "channel": channel, "data": msg})
                
        return q

    def unsubscribe(self, channel: str, q: asyncio.Queue):
        if channel in self.subscribers and q in self.subscribers[channel]:
            self.subscribers[channel].remove(q)

    def psubscribe(self, pattern: str) -> asyncio.Queue:
        if pattern not in self.psubscribers:
            self.psubscribers[pattern] = []
        q = asyncio.Queue()
        self.psubscribers[pattern].append(q)
        return q

    def punsubscribe(self, pattern: str, q: asyncio.Queue):
        if pattern in self.psubscribers and q in self.psubscribers[pattern]:
            self.psubscribers[pattern].remove(q)

pubsub_manager = InMemoryPubSub()

async def publish_event(channel: str, event_type: str, data: dict):
    payload = {
        "type": event_type,
        "data": data
    }
    await pubsub_manager.publish(channel, json.dumps(payload))

async def subscribe_events(channel: str) -> AsyncGenerator[dict, None]:
    q = pubsub_manager.subscribe(channel)
    try:
        while True:
            msg = await q.get()
            yield json.loads(msg['data'])
    except asyncio.CancelledError:
        pass
    finally:
        pubsub_manager.unsubscribe(channel, q)

async def psubscribe_events(pattern: str) -> AsyncGenerator[dict, None]:
    q = pubsub_manager.psubscribe(pattern)
    try:
        while True:
            msg = await q.get()
            yield json.loads(msg['data'])
    except asyncio.CancelledError:
        pass
    finally:
        pubsub_manager.punsubscribe(pattern, q)
