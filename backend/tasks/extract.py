from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from utils.logger import log

import utils.db as db
import core.parse as parse
import core.chunk as chunk
import apis.elastic_search as elastic_search

app = Celery('extract', broker='pyamqp://guest@localhost//')

# Extract: Step 1 - Parsing
@app.task
def parse_task(file_path):
    file_data = parse.parse_file(file_path)
    file_id = db.save_file(file_data)

    app.send_task("tasks.extract.chunk_task", args=[file_id])

# Extract: Step 2 - Chunking
@app.task
def chunk_task(file_id):
    file_data = db.read_file(file_id)
    if file_data:
        chunk_ids = []
        chunks = chunk.chunkify(file_data.content)
        start_position = 0
        for chunk_text in chunks:
            chunk_id = db.save_chunk(file_id, chunk_text, start_position)
            chunk_ids.append(chunk_id)
            start_position += len(chunk_text)

        app.send_task("tasks.extract.index_task", args=[file_id])

# Extract: Step 3 - Indexing
@app.task
def index_task(file_id):
    chunks_data = db.read_chunks_of_file(file_id)

    # TODO: Refactor the following part, pass the chunks directly
    chunks = []
    chunk_ids = []
    for chunk in chunks_data:
        chunks.append(chunk.chunk_text)
        chunk_ids.append(chunk.chunk_id)

    elastic_search.save(chunks, chunk_ids)
    # faiss.save(chunks, chunk_ids)

@worker_process_init.connect
def init(*args, **kwargs):
    try:
      db.init()
      chunk.init()
      elastic_search.init()
    except Exception as exc:
      log.error("Exception while initialising extract pipeline", exc)

@worker_process_shutdown.connect
def shutdown(*args, **kwargs):
    db.terminate()
    elastic_search.terminate()
