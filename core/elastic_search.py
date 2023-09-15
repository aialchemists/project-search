from elasticsearch import Elasticsearch
from typing import List

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

def create_inverted_index(chunks, chunk_ids) -> List[float]:
    # Initialize an Elasticsearch client

    # Creating mapping
    mappings = {
        "properties": {
            "chunk_text": {"type": "text", "analyzer": "standard"}
        }
    }

    # Deleting indexes (if exists)
    if es.indices.exists(index='chunks'):
        es.indices.delete(index='chunks')

    es.indices.create(index="chunks", mappings=mappings)

    # Index the chunks
    for idx, chunk in enumerate(chunks):
        doc = {
            "chunk_text": chunk
        }
        es.index(index="chunks", id=chunk_ids[idx], document=doc)

    # Print chunks to see format
    # print(es.indices.get(index="*"))

    es.indices.refresh(index="chunks")

def search_chunks(user_query):
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
    results = es.search(index="chunks", query=search_query)

    # Process and return the search results
    search_results = []
    for hit in results['hits']['hits']:
        source = hit['_source']
        search_results.append({
            "document_id": hit['_id'],
            "score": hit['_score'],
            "source": source
        })

    print(search_results)

    return search_results
