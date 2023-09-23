from utils.logger import log

from elasticsearch import Elasticsearch
from typing import List

from db.chunk import ChunkData

INDEX_NAME = 'chunks'

es: Elasticsearch

def init():
    log.info(f"Initialising Elasticsearch")
    global es
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
    log.info('Elasticsearch initialised')

def terminate():
    es.transport.close()

def migrate():
    # Deleting indexes (if exists)
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        log.info(f"Deleted elastic search index named {INDEX_NAME}")

    mappings = {
        "properties": {
            "chunk_text": {"type": "text", "analyzer": "standard"}
        }
    }
    # Creating chunks indices
    es.indices.create(index=INDEX_NAME, mappings=mappings)
    log.info(f"Created elastic search index named {INDEX_NAME}")

def save(chunks: List[ChunkData]):
    # Index the chunks
    for chunk in chunks:
        doc = {
            "chunk_text": chunk.chunk_text
        }
        es.index(index=INDEX_NAME, id=chunk.chunk_id, document=doc)

    es.indices.refresh(index=INDEX_NAME)

def search(user_query, top_k) -> List[int]:
    # Define search query
    search_query = {
        "match": {
            "chunk_text": {
                "query": user_query,
                "fuzziness": "AUTO"
            }
        }
    }

    # Execute the search
    results = es.search(index=INDEX_NAME, query=search_query, sort=["_score:desc"], size= top_k)

    # Process and return the search results
    chunk_ids = []
    for hit in results['hits']['hits']:
        chunk_ids.append(int(hit['_id']))
    return chunk_ids
