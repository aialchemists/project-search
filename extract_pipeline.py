import os

from core.parse import parse_file
from core.chunk import chunkify
from core.embedding import embed_text
import core.elastic_search as elastic_search
import core.db as db

def process_local_file(file_path):
    # Step 1: Parse
    file_data = parse_file(file_path)
    file_id = db.save_file(file_data)

    # Step 2: Chunking
    chunk_ids = []
    chunks = chunkify(file_data.content)
    start_position = 0
    for chunk_text in chunks:
        embedding = embed_text(chunk_text)
        chunk_id = db.save_chunk(file_id, chunk_text, embedding, start_position)
        chunk_ids.append(chunk_id)
        start_position += len(chunk_text)

    # Step 3: Create the inverted index with Elasticsearch
    elastic_search.save(chunks, chunk_ids)

def process_local_dir(directory_path):
    if not os.path.exists(directory_path):
        print(f"'{directory_path}' is not a valid directory path.")

    file_paths = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, filename))]
    for path in file_paths:
        if not os.path.basename(path).startswith("."):
            process_local_file(path)

process_local_dir("./data/")
