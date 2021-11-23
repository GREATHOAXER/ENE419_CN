import websockets
import asyncio
import json


async def main():
    async with websockets.connect("wss://api.upbit.com/websocket/v1")
if __name__ == '__main__':
    asyncio.run(main())