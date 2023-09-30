import re
import json

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from utils.logger import log
from utils.file import FileType

import db
from db.file import save_file, read_file
from db.chunk import save_chunk, read_chunks_of_file
from db.metadata import save_meta

import core.chunk as chunk
import apis.elastic_search as elastic_search
import apis.vfaiss as vfaiss
import apis.parse as parse

app = Celery('extract', broker='pyamqp://guest@localhost//')

# Extract: Step 1 - Parsing
@app.task
def parse_task(file_path):
    file_data, metadata = parse.parse_file(file_path)
    file_id = save_file(file_data)
    save_meta(file_id, metadata)

    if file_data.file_type in [FileType.TEXT, FileType.IMAGE]:
        app.send_task("tasks.extract.chunk_task", args=[file_id])
    elif file_data.file_type in [FileType.AUDIO, FileType.VIDEO]:
        app.send_task("tasks.extract.chunk_av_task", args=[file_id])

# Extract: Step 2 - Chunking
@app.task
def chunk_task(file_id):
    file_data = read_file(file_id)
    if file_data:
        content = json.loads(file_data.content)
        chunks = chunk.chunkify(content)
        start_position = 0
        for chunk_text in chunks:
            if re.search('[a-zA-Z]', chunk_text):
                save_chunk(file_id, chunk_text, start_position, len(chunk_text))
            start_position += len(chunk_text)

        app.send_task("tasks.extract.index_task", args=[file_id])

@app.task
def chunk_av_task(file_id):
    file_data = read_file(file_id)
    if file_data:
        content = json.loads(file_data.content)
        for chunk in content:
            save_chunk(file_id, chunk["text"], chunk["start_time"], chunk["end_time"] - chunk["start_time"])

        app.send_task("tasks.extract.index_task", args=[file_id])

# Extract: Step 3 - Indexing
@app.task
def index_task(file_id):
    chunks = read_chunks_of_file(file_id)
    elastic_search.save(chunks)
    vfaiss.save(chunks)

@worker_process_init.connect
def init(*args, **kwargs):
    try:
      db.init()
      parse.init()
      chunk.init()
      elastic_search.init()
      vfaiss.init()
      log.info("--- Tasks initialised ------------------------------")
    except Exception as exc:
      log.error("Exception while initialising extract pipeline", exc)

@worker_process_shutdown.connect
def shutdown(*args, **kwargs):
    db.terminate()
    elastic_search.terminate()
