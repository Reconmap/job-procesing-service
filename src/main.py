#!/usr/bin/env python

import asyncio
import websockets
import sys
import signal
import logging

from redis import consume_redis_queue
from network import register_client, close_client_connections

def signal_handler(signal, frame):
    logging.info("Exitting gracefully...")
    loop.stop()
    close_client_connections()
    sys.exit(0)

logging.basicConfig(filename='logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

signal.signal(signal.SIGINT, signal_handler)

loop = asyncio.get_event_loop()

if __name__ == "__main__":
    serve_ws_requests = websockets.serve(register_client, "0.0.0.0", 8765)

    tasks = asyncio.wait([consume_redis_queue(), serve_ws_requests])
    loop.run_until_complete(tasks)
    loop.close()

