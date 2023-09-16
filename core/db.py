# pip install psycopg2-binary

from pathlib import Path
import os

import psycopg2
import json
from typing import List

from .file_data import FileData
from utils.configs import db_configs

try:
  conn = psycopg2.connect(db_configs.get_dsn())
except Exception as exc:
  print(exc)
  print("I am unable to connect to the database")
  raise exc

def migrate():
    schema = Path(os.getcwd()).joinpath('core/db_schema.sql').read_text()
    with conn.cursor() as cursor:
        cursor.execute(schema)
        conn.commit()
        return schema

def save_file(data: FileData) -> int:
    with conn.cursor() as cursor:
        metadata = json.dumps(data.metadata)
        cursor.execute("INSERT INTO file (file_path, content, metadata) "
                        "VALUES (%s,%s,%s) RETURNING *", (data.file_path, data.content, metadata))
        conn.commit()

        inserted_row = cursor.fetchone()
        if inserted_row:
          print(f"Saved details of file {data.file_path}")
          return inserted_row[0]
        else:
          raise Exception("Insert into file table failed")

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

def close():
    conn.close()
