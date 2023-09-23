from utils.logger import log
from typing import List

from fastapi import FastAPI
from starlette.responses import RedirectResponse

import apis.vfaiss as vfaiss
import apis.elastic_search as elastic_search
import core.cross_encoder as cross_encoder
import apis.rerank as rerank_api

import db
from db.metadata import read_meta

from utils.configs import configs

app = FastAPI(title="Vector Search - APIs")

try:
    db.init()
    cross_encoder.init()
    elastic_search.init()
    rerank_api.init()
    vfaiss.init()
except Exception as exc:
    log.error("Exception while initialising extract pipeline", exc)

@app.get("/", include_in_schema=False)
async def root_api():
    response = RedirectResponse(url='/docs')
    return response

@app.get("/api/configs")
async def configs_api():
    return configs

def get_facets(file_ids) -> List:
    metadatas = read_meta(list(file_ids))
    facet_map = {}
    for meta in metadatas:
        if not meta.meta_key in facet_map:
            facet_map[meta.meta_key] = set()
        facet_map[meta.meta_key].add(meta.meta_value)

    facets = []
    facets.append({
        "title": "File Type",
        "values": list(facet_map["file_type"])
    })
    facets.append({
        "title": "Year",
        "values": list(facet_map["year"])
    })
    return facets

@app.get("/api/search")
async def search_api(query):
    top_k = 10

    chunk_ids = []
    elastic_ids = elastic_search.search(query, top_k)
    chunk_ids.extend(elastic_ids)
    semantic_ids = vfaiss.search(query, top_k)
    chunk_ids.extend(semantic_ids)
    chunk_ids = list(set(chunk_ids))

    results = await rerank_api.rerank_chunks(query, chunk_ids)

    file_ids = set()
    for result in results:
        file_ids.add(result["file_id"])
        result["semantic_match"] = result["chunk_id"] in semantic_ids
        result["lexical_match"] = result["chunk_id"] in elastic_ids

    return {
      "results": results,
      "facets": get_facets(file_ids)
    }

@app.get("/files/{file_path}")
async def files_api(file_path):
    return {
      "file_path": file_path
    }
