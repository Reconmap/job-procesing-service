#!/usr/bin/env python

import asyncio
import websockets
import json
import sys
import signal
import logging
import aioredis

async def broadcast(item):
    try:
        for client in client_set:
            await client.send(json.dumps(item))
    except e:
        logging.exception(e)

async def consume_redis_queue():
    r = await aioredis.create_redis_pool('redis://redis', password = 'REconDIS')
    while True:
        itemEncoded = await r.brpop('tasks:queue')
        item = json.loads(itemEncoded[1].decode('utf-8'))
        await broadcast(item)

async def unregister_client(websocket):
    logging.info("unregistering client")
    client_set.remove(websocket)

async def register_client(websocket, path):
    logging.info("new client registered")
    try:
        while True:
            client_set.add(websocket)
            name = await websocket.recv()
    finally:
        await unregister_client(websocket)

def signal_handler(signal, frame):
    logging.info("Exitting gracefully...")
    loop.stop()
    for client in client_set:
        client.close()
    sys.exit(0)

logging.basicConfig(filename='logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

signal.signal(signal.SIGINT, signal_handler)

loop = asyncio.get_event_loop()

client_set = set()

if __name__ == "__main__":
    serve_ws_requests = websockets.serve(register_client, "0.0.0.0", 8765)

    tasks = asyncio.wait([consume_redis_queue(), serve_ws_requests])
    loop.run_until_complete(tasks)
    loop.close()

