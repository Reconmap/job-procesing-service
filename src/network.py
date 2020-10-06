import json
import logging

client_set = set()

async def broadcast(item):
    try:
        for client in client_set:
            await client.send(json.dumps(item))
    except Exception as e:
        logging.exception(e)

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

def close_client_connections():
    for client in client_set:
        client.close()

