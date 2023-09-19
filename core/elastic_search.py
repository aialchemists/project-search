from utils.logger import log

from elasticsearch import Elasticsearch
from typing import List

es: Elasticsearch

def init():
    log.info(f"Initialising Elasticsearch")
    global es
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
    log.info('Elasticsearch initialised')

def migrate():
    # Deleting indexes (if exists)
    if es.indices.exists(index='chunks'):
        es.indices.delete(index='chunks')

    mappings = {
        "properties": {
            "chunk_text": {"type": "text", "analyzer": "standard"}
        }
    }
    # Creating chunks indices
    es.indices.create(index="chunks", mappings=mappings)

def save(chunks, chunk_ids) -> List[float]:
    # Index the chunks
    for idx, chunk in enumerate(chunks):
        doc = {
            "chunk_text": chunk
        }
        es.index(index="chunks", id=chunk_ids[idx], document=doc)

    es.indices.refresh(index="chunks")

def search(user_query, top_k):
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
    results = es.search(index="chunks", query=search_query, sort=["_score:desc"], size= top_k)

    # Process and return the search results
    search_results = []
    for hit in results['hits']['hits']:
        source = hit['_source']
        search_results.append({
            "document_id": hit['_id'],
            "score": hit['_score'],
            "source": source
        })
    return search_results

