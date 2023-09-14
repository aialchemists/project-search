import os

from core.tika import parse_file
from core.chunk import chunkify
from core.db import DB
from core.embedding import embed_text

def process_local_file(file_path, db: DB):
    # Step 1
    file_data = parse_file(file_path)
    file_id = db.save_file(file_data)

    # Step 2
    chunks = chunkify(file_data.content)
    start_position = 0
    for chunk_text in chunks:
        embedding = embed_text(chunk_text)
        db.save_chunk(file_id, chunk_text, embedding, start_position)
        start_position += len(chunk_text)

def process_local_dir(directory_path):
    if not os.path.exists(directory_path):
        print(f"'{directory_path}' is not a valid directory path.")

    db = DB()
    file_paths = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, filename))]
    for path in file_paths:
        if not os.path.basename(path).startswith("."):
            process_local_file(path, db)

process_local_dir("./data/")
