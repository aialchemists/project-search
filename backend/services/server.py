from utils.logger import log

from fastapi import FastAPI
from starlette.responses import RedirectResponse

import core.elastic_search as elastic_search
import core.cross_encoder as cross_encoder
import utils.db as db

from utils.configs import configs

app = FastAPI(title="Vector Search - APIs")

try:
  db.init()
  cross_encoder.init()
  elastic_search.init()
except Exception as exc:
  log.error("Exception while initialising extract pipeline", exc)

@app.get("/", include_in_schema=False)
async def root_api():
    response = RedirectResponse(url='/docs')
    return response

@app.get("/api/configs")
async def configs_api():
    return configs

@app.get("/api/search")
async def search_api(query):
    top_k = 10
    search_results = elastic_search.search(query, top_k)

    chunk_ids = list(map(lambda r: r["document_id"], search_results))
    chunks = db.read_chunks(chunk_ids)
    chunk_texts = list(map(lambda c: c.chunk_text, chunks))

    top_pairs = cross_encoder.rank(query, chunk_texts, top_k)

    results = []
    for pair in top_pairs:
        results.append({
            "text": pair[0][1],
            "file_path": "./path/to/TestFile.pdf",
            "score": pair[1].item()
        })

    return {
      "results": results,
      "facets": []
    }

@app.get("/files/{file_path}")
async def files_api(file_path):
    return {
      "file_path": file_path
    }
