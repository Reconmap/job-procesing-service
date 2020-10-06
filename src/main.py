#!/usr/bin/env python

import asyncio
import websockets
import sys
import signal
import logging
import os

from redis import consume_redis_queue
from network import register_client, close_client_connections

def signal_handler(signal, frame):
    logging.info("Exitting gracefully...")
    loop.stop()
    close_client_connections()
    sys.exit(0)

dir_path = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename=dir_path + '/../logs/app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

signal.signal(signal.SIGINT, signal_handler)

loop = asyncio.get_event_loop()

if __name__ == "__main__":
    valid_origins = os.getenv("VALID_ORIGINS").split(',')
    serve_ws_requests = websockets.serve(register_client, "0.0.0.0", 8765, origins = valid_origins)

    tasks = asyncio.wait([consume_redis_queue(), serve_ws_requests])
    loop.run_until_complete(tasks)
    loop.close()

