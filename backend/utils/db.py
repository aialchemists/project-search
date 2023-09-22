from utils.logger import log

import os
from pathlib import Path
from dataclasses import dataclass

# TODO: Use SQLmodel instead of Psycopg2
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection

import json
from typing import List, Union

from core.file_data import FileData
from utils.configs import db_configs

conn: connection

def init():
    log.info("Establishing database connection")
    global conn
    conn = connect(db_configs.get_dsn())
    log.info('Database connection established')

def terminate():
   conn.close()

def migrate():
    schema = Path(os.getcwd()).joinpath('utils/db_schema.sql').read_text()
    with conn.cursor() as cursor:
        cursor.execute(schema)
        conn.commit()
        return schema

def save_file(data: FileData) -> int:
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO file (file_path, content) VALUES (%s,%s) RETURNING *", (data.file_path, data.content))
        conn.commit()

        inserted_row = cursor.fetchone()
        if inserted_row:
          log.info(f"Saved details of file {data.file_path}")
          return inserted_row[0]
        else:
          raise Exception("Insert into file table failed")

def read_file(file_id: int) -> Union[FileData, None]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM file WHERE file_id = %s", (file_id,))
        row = cursor.fetchone()
        return FileData(**row) if row else None

@dataclass
class Chunk:
   chunk_id: int
   file_id: int
   chunk_text: str
   start_position: int
   length: int

def save_chunk(file_id: int, chunk_text: str, start_position: int):
    chunk_length = len(chunk_text)
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO chunk (file_id, chunk_text, start_position, length) VALUES (%s,%s,%s,%s) RETURNING *", (file_id, chunk_text, start_position, chunk_length))
        conn.commit()

        inserted_row = cursor.fetchone()
        if inserted_row:
          log.info(f"Saved chunk of file id {file_id} from position {start_position}")
          return inserted_row[0]
        else:
          raise Exception("Insert into chunk table failed")

def read_chunks(chunk_ids: List[str]) -> List[Chunk]:
    ids = tuple(chunk_ids)
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM chunk WHERE chunk_id IN %s", (ids,))
        rows = cursor.fetchall()
        return list(map(lambda r: Chunk(**r), rows))

def read_chunks_of_file(file_id: int) -> List[Chunk]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM chunk WHERE file_id = %s", (file_id,))
        rows = cursor.fetchall()
        return list(map(lambda r: Chunk(**r), rows))

def close():
    conn.close()
