import asyncio

from utils.logger import log
import db
from db.chunk import read_chunks
import core.cross_encoder as cross_encoder

from utils.action_rpc.server import ARPCServer

def rerank(data: dict) -> dict:
    chunks = []
    chunk_ids = data["chunk_ids"]
    min_score = data["min_score"]
    log.info(f"Reranking chunks - {chunk_ids}")

    chunk_datas = read_chunks(chunk_ids)
    if len(chunk_datas) > 0:
        chunk_texts = list(map(lambda c: c.chunk_text, chunk_datas))
        chunk_ids = list(map(lambda c: c.chunk_id, chunk_datas))

        top_pairs = cross_encoder.rank(data["user_query"], chunk_texts, chunk_ids, data["top_k"])

        for pair in top_pairs:
            score = pair[1].item()
            if score >= min_score:
                chunks.append({
                    "chunk_id": pair[2],
                    "file_path": "./path/to/TestFile.pdf",
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
