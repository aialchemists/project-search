import asyncio
import dataclasses

from utils.logger import log

import core.parse as parse
from utils.action_rpc.server import ARPCServer

def parse_handler(data: dict) -> dict:
    file_data, metadata = parse.parse_file(data["file_path"])
    return {
        "file_data": dataclasses.asdict(file_data),
        "metadata": metadata
    }

async def start_server():
    log.info("Initialising parse service")
    parse.init()

    server = ARPCServer("50052")
    server.register_action("parse", parse_handler)
    await server.start()

if __name__ == "__main__":
   asyncio.run(start_server())
