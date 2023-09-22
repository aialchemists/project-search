from utils.logger import log
import os

import utils.db as db
import core.parse as parse
import core.chunk as chunk
import core.embed as embed
import apis.elastic_search as elastic_search

try:
  db.init()
  chunk.init()
  embed.init()
  elastic_search.init()
except Exception as exc:
  log.error("Exception while initialising extract pipeline", exc)

def process_local_file(file_path):
    # Step 1: Parse
    file_data = parse.parse_file(file_path)
    file_id = db.save_file(file_data)

    # Step 2: Chunking
    chunk_ids = []
    chunks = chunk.chunkify(file_data.content)
    start_position = 0
    for chunk_text in chunks:
        embedding = embed.embed_text(chunk_text)
        chunk_id = db.save_chunk(file_id, chunk_text, embedding, start_position)
        chunk_ids.append(chunk_id)
        start_position += len(chunk_text)

    # Step 3: Create the inverted index with Elasticsearch
    elastic_search.save(chunks, chunk_ids)

def process_local_dir(directory_path):
    if os.path.isdir(directory_path):
        file_paths = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, filename))]
        for path in file_paths:
            if not os.path.basename(path).startswith("."):
                process_local_file(path)
    else:
        log.error(f"'{directory_path}' is not a valid directory path.")

process_local_dir("./data/")
