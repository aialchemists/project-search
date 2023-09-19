# pip install psycopg2-binary

from pathlib import Path
import os
from dataclasses import dataclass
import logging as log

import psycopg2
from psycopg2.extras import RealDictCursor

import json
from typing import List

from core.file_data import FileData
from utils.configs import db_configs

try:
  log.info("Connecting to the database")
  conn = psycopg2.connect(db_configs.get_dsn())
except Exception as exc:
  print(exc)
  log.error(exc)
  print("I am unable to connect to the database")
  raise exc

def migrate():
    schema = Path(os.getcwd()).joinpath('utils/db_schema.sql').read_text()
    with conn.cursor() as cursor:
        cursor.execute(schema)
        conn.commit()
        return schema

def save_file(data: FileData) -> int:
    with conn.cursor() as cursor:
        metadata = json.dumps(data.metadata)
        cursor.execute("INSERT INTO file (file_path, content) "
                        "VALUES (%s,%s) RETURNING *", (data.file_path, data.content))
        conn.commit()

        inserted_row = cursor.fetchone()
        if inserted_row:
          print(f"Saved details of file {data.file_path}")
          return inserted_row[0]
        else:
          raise Exception("Insert into file table failed")

@dataclass
class Chunk:
   chunk_id: int
   file_id: int
   chunk_text: str
   embedding: List[float]
   start_position: int
   length: int

def save_chunk(file_id: int, chunk_text: str, embedding: List[float], start_position: int):
    chunk_length = len(chunk_text)
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO chunk (file_id, chunk_text, embedding, start_position, length) "
                        "VALUES (%s,%s,%s,%s,%s) RETURNING *",
                        (file_id, chunk_text, embedding, start_position, chunk_length))
        conn.commit()

        inserted_row = cursor.fetchone()
        if inserted_row:
          print(f"Saved chunk of file id {file_id} from position {start_position}")
          return inserted_row[0]
        else:
          raise Exception("Insert into chunk table failed")

def read_chunks(chunk_ids: List[str]) -> List[Chunk]:
    ids = tuple(chunk_ids)
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM chunk WHERE chunk_id IN %s", (ids,))
        rows = cursor.fetchall()
        return list(map(lambda r: Chunk(**r), rows))

def close():
    conn.close()
