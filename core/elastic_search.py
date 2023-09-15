# Need to integrate with remaining code, pass user_query

from elasticsearch import Elasticsearch

def create_inverted_index(text):
    # Initialize an Elasticsearch client
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

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
    for chunk in text:
        doc = {
            "chunk_text": chunk["text"]
        }
        es.index(index="chunks", id=chunk["chunk_id"], document=doc)

    return es

def search_chunks(es, user_query):
    # Define search query
    search_query = {
        "match": {
            "chunk_text": {
                "query": user_query,
                "fuzziness": "AUTO"
            }
        }
    }

    es.indices.refresh(index="chunks")

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

    return search_results

# Example usage:
# chunks_to_create = [
#     {'chunk_id': 1, 'text': 'Popcorn kernels are popping in the oven. I always enjoy popcorn while watching a movie.'},
#     {'chunk_id': 2, 'text': 'There was a class on Machine Learning at SupportVectors.'},
#     {'chunk_id': 3, 'text': 'I went to Ross and Walmart after work today. I got milk and a jacket.'},
# ]
#
# es = create_inverted_index(chunks_to_create)
#
# user_query = "Movie"
# results = search_chunks(es, user_query)
# for result in results:
#     print(f"Document ID: {result['document_id']}, Score: {result['score']}, Source: {result['source']}")
