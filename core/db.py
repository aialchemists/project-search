# pip install psycopg2-binary

from pathlib import Path
import os

import psycopg2
import json

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

    def save_file(self, data: FileData):
        with self.conn.cursor() as cursor:
            metadata = json.dumps(data.metadata)
            cursor.execute("INSERT INTO files VALUES (%s,%s,%s)", (data.id, data.file_name, metadata))
            self.conn.commit()
            print(f"Saved details of file {data.file_name}")

    def save_chunk(self, data: FileData, chunk_text: str, start_position: int):
        file_id = data.id
        chunk_length = len(chunk_text)
        with self.conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO chunks (file_id, chunk_text, start_position, length) VALUES (%s,%s,%s,%s)", (file_id, chunk_text, start_position, chunk_length))
            self.conn.commit()
            print(f"Saved chunk of file {file_id}")

    def close(self):
        self.conn.close()
