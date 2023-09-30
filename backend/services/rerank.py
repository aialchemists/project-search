import asyncio
from typing import List, Dict

from utils.logger import log
import db
from db.chunk import read_chunks, ChunkData
from db.file import read_file
import core.cross_encoder as cross_encoder

from utils.action_rpc.server import ARPCServer

def get_chunk_map(chunks: List[ChunkData]) -> Dict[int, ChunkData]:
    map = {}
    for chunk in chunks:
        map[chunk.chunk_id] = chunk
    return map

def rerank(data: dict) -> dict:
    chunks = []
    chunk_ids = data["chunk_ids"]
    min_score = data["min_score"]
    log.info(f"Reranking chunks - {chunk_ids}")

    chunk_datas = read_chunks(chunk_ids)
    if len(chunk_datas) > 0:
        chunk_texts = list(map(lambda c: c.chunk_text, chunk_datas))
        chunk_ids = list(map(lambda c: c.chunk_id, chunk_datas))

        chunk_map = get_chunk_map(chunk_datas)

        top_pairs = cross_encoder.rank(data["user_query"], chunk_texts, chunk_ids, data["top_k"])

        for pair in top_pairs:
            chunk_id = pair[2]
            file_data = read_file(chunk_map[chunk_id].file_id)

            score = pair[1].item()
            if score >= min_score:
                chunks.append({
                    "chunk_id": chunk_id,
                    "file_type": file_data.file_type if file_data else None,
                    "file_id": file_data.file_id if file_data else None,
                    "file_path": file_data.file_path if file_data else "",
                    "text": pair[0][1],
                    "score": score
                })

    return {
        "chunks": chunks
    }

async def start_server():
    db.init()
    cross_encoder.init()

    server = ARPCServer("50051")
    server.register_action("rerank", rerank)
    await server.start()

if __name__ == "__main__":
   asyncio.run(start_server())
