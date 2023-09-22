import asyncio

from utils.logger import log
import utils.db as db
import core.cross_encoder as cross_encoder

from utils.action_rpc.server import ARPCServer

def rerank(data: dict) -> dict:
    chunk_ids = data["chunk_ids"]
    log.info(f"Reranking chunks - {chunk_ids}")

    chunks = db.read_chunks(chunk_ids)
    chunk_texts = list(map(lambda c: c.chunk_text, chunks))
    top_pairs = cross_encoder.rank(data["user_query"], chunk_texts, data["top_k"])

    chunks = []
    for pair in top_pairs:
        chunks.append({
            "file_path": "./path/to/TestFile.pdf",
            "text": pair[0][1],
            "score": pair[1].item()
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
