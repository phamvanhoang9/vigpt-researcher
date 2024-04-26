import asyncio
import websockets

# This code sets up a WebSocket server that echoes back any message it receives from clients.
# Websockets create real-time applications such as chat servers, real-time data visualization, multiplayer games, and more.

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

