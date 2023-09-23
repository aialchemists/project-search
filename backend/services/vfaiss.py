import asyncio

from utils.logger import log
import core.vfaiss as vfaiss

from utils.action_rpc.server import ARPCServer

def save(data):
    vfaiss.build_index(data["chunk_texts"], data["chunk_ids"])

def search(data):
    return {
        "chunk_ids": vfaiss.search_index(data["query"], data["top_k"])
    }

async def start_server():
    vfaiss.init()

    server = ARPCServer("6000")
    server.register_action("save", save)
    server.register_action("search", search)
    await server.start()

if __name__ == "__main__":
   asyncio.run(start_server())
