# pip install psycopg2-binary

from pathlib import Path
import os

import psycopg2
import json
from typing import List

from .file_data import FileData
from utils.configs import db_configs

_SCHEMA = Path(os.getcwd()).joinpath('core/db_schema.sql').read_text()

def _init_connection():
    try:
      conn = psycopg2.connect(db_configs.get_dsn())
      return conn
    except Exception as exc:
      print(exc)
      print("I am unable to connect to the database")
      raise exc

class DB:
    def __init__(self):
        self.conn = _init_connection()

    def migrate(self):
        with self.conn.cursor() as cursor:
            cursor.execute(_SCHEMA)
            self.conn.commit()
            return _SCHEMA

    def save_file(self, data: FileData) -> int:
        with self.conn.cursor() as cursor:
            metadata = json.dumps(data.metadata)
            cursor.execute("INSERT INTO file (file_path, content, metadata) "
                           "VALUES (%s,%s,%s) RETURNING *", (data.file_path, data.content, metadata))
            self.conn.commit()

            inserted_row = cursor.fetchone()
            if inserted_row:
              print(f"Saved details of file {data.file_path}")
              return inserted_row[0]
            else:
              raise Exception("Insert into file table failed")

    def save_chunk(self, file_id: int, chunk_text: str, embedding: List[float], start_position: int):
        chunk_length = len(chunk_text)
        with self.conn.cursor() as cursor:
            cursor.execute("INSERT INTO chunk (file_id, chunk_text, embedding, start_position, length) "
                           "VALUES (%s,%s,%s,%s,%s) RETURNING *",
                           (file_id, chunk_text, embedding, start_position, chunk_length))
            self.conn.commit()

            inserted_row = cursor.fetchone()
            if inserted_row:
              print(f"Saved chunk of file id {file_id} from position {start_position}")
              return inserted_row[0]
            else:
              raise Exception("Insert into chunk table failed")

    def close(self):
        self.conn.close()
