from typing import List
from utils.action_rpc.client import ARPCClient

client: ARPCClient

def init():
    global client
    client = ARPCClient("localhost:50051")

def rerank_chunks(user_query: str, chunk_ids: List[str]):
    resp = client.call("rerank", {
      "user_query": user_query,
      "chunk_ids": chunk_ids,
      "top_k": 10
    })
    return resp["chunks"]
