import json
import asyncio
import socket
import sqlalchemy

from workspace import workspace

from websockets.asyncio.server import serve

from modules.logging import logger

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import func

from database.models import Users

from functools import partial

sqlEngine = sqlalchemy.create_engine(workspace.getConfigAttribute("RestlessDatabaseFilePath"))

connections = {}

log: logger = logger("websocket-proxy-service.log", "INFO")

async def sendToReverseProxy(message, reader, writer):
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(1024)

    return data.decode()

async def proxyServer(websocket, reader, writer):
    async for message in websocket:
        event = json.loads(message)

        userFound: bool = False
        stmt = select(func.count()).select_from(Users).where(Users.username == event["username"]).where(Users.pincode  == event["pincode"])
        with Session(sqlEngine) as session:
            userFound = True if session.execute(stmt).scalar_one() > 0 else False

        if not userFound:
            await websocket.close()
            return

        response = await sendToReverseProxy(event["data"], reader, writer)

        print(f"[/] Data received :: {event['data']} . . .")
        log.info(f"Data received :: {event['data']} . . .")

        if len(response) > 0:
            await websocket.send(response)
            log.info(f"Response sent back :: {response} . . .")

async def main() -> None:
    log.info("Started")
    proxyReader, proxyWriter = await asyncio.open_connection("<YOUR_IP>", 12444)
    async with serve(partial(proxyServer, reader=proxyReader, writer=proxyWriter), "localhost", 13000):
        await asyncio.get_running_loop().create_future()
    log.info("Finished")

def runMain():
    asyncio.run(main())

if __name__ == "__main__":
    runMain()
