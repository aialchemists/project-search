# pip install psycopg2-binary

import psycopg2
import json

from .file_data import FileData

def _init_connection():
    try:
      conn = psycopg2.connect("dbname='llm_vdb' user='postgres' host='localhost' port='5431' password='mysecretpassword'")
      print("Connected to the database")
      return conn
    except Exception as exc:
      print(exc)
      print("I am unable to connect to the database")
      raise exc

class DB:
    def __init__(self):
        self.conn = _init_connection()

    def save_file(self, data: FileData):
        with self.conn.cursor() as cursor:
            metadata = json.dumps(data.metadata)
            cursor.execute(f"INSERT INTO files VALUES (%s,%s,%s)", (data.id, data.file_name, metadata))
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
