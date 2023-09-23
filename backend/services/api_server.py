from utils.logger import log

from fastapi import FastAPI
from starlette.responses import RedirectResponse

import apis.elastic_search as elastic_search
import core.cross_encoder as cross_encoder
import apis.rerank as rerank_api
import db

from utils.configs import configs

app = FastAPI(title="Vector Search - APIs")

try:
  db.init()
  cross_encoder.init()
  elastic_search.init()
  rerank_api.init()
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
    results = await rerank_api.rerank_chunks(query, chunk_ids)

    return {
      "results": results,
      "facets": []
    }

@app.get("/files/{file_path}")
async def files_api(file_path):
    return {
      "file_path": file_path
    }
