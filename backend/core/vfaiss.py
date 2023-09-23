import os
from typing import List

from utils.logger import log
from utils.configs import embedding_configs

import faiss 
from sentence_transformers import SentenceTransformer

FILE_PATH = "large.index"

model: SentenceTransformer
index: faiss.IndexIDMap

def init():
    log.info(f"Initialising embedding model {embedding_configs.model}")
    global model
    model = SentenceTransformer(embedding_configs.model)
    log.info('Embedding model initialised')

    global index
    if os.path.isfile(FILE_PATH):
        index = faiss.read_index(FILE_PATH)
        log.info('Loaded index from file')
    else:
        l2_index = faiss.IndexFlatL2(model.get_sentence_embedding_dimension())
        index = faiss.IndexIDMap(l2_index)
        log.info('Created new index')

def build_index(chunk_texts, chunk_ids):
    corpus_vector = model.encode(chunk_texts)
    index.add_with_ids(corpus_vector, chunk_ids)

    faiss.write_index(index, FILE_PATH)

def search_index(query, top_k) -> List[int]:
    query_vectors = model.encode([query])
    distance, ids = index.search(query_vectors, top_k)

    ids = ids[0].tolist()
    ids = [i for i in ids if i != -1]
    return ids
