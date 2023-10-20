from typing import List
from utils.action_rpc.client import ARPCClient

client: ARPCClient

def init():
    global client
    client = ARPCClient("localhost:50051")

async def rerank_chunks(user_query: str, chunk_ids: List[str]):
    if len(chunk_ids) == 0:
        return []

    resp = await client.call("rerank", {
      "user_query": user_query,
      "chunk_ids": chunk_ids,
      "top_k": 10,
      "min_score": 0.2 # TODO: Make a configuration
    })
    return resp["chunks"]
