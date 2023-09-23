from typing import List
from utils.action_rpc.client import ARPCClientSync

from db.chunk import ChunkData

client: ARPCClientSync

def init():
    global client
    client = ARPCClientSync("localhost:6000")

def save(chunks: List[ChunkData]):
    chunk_ids = []
    chunk_texts = []

    for chunk in chunks:
        chunk_ids.append(chunk.chunk_id)
        chunk_texts.append(chunk.chunk_text)

    client.call("save", {
        "chunk_ids": chunk_ids,
        "chunk_texts": chunk_texts
    })

def search(query, top_k) -> List[int]:
    resp = client.call("search", {
        "query": query,
        "top_k": top_k
    })
    return resp["chunk_ids"]
