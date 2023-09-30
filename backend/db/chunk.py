from dataclasses import dataclass
from utils.logger import log

from . import get_conn
from psycopg2.extras import RealDictCursor

from typing import List

@dataclass
class ChunkData:
   chunk_id: int
   file_id: int
   chunk_text: str
   start_position: int
   length: int

def save_chunk(file_id: int, chunk_text: str, start_position: int, length: int):
    with get_conn().cursor() as cursor:
        cursor.execute("INSERT INTO chunk (file_id, chunk_text, start_position, length) VALUES (%s,%s,%s,%s) RETURNING *", (file_id, chunk_text, start_position, length))
        get_conn().commit()

        inserted_row = cursor.fetchone()
        if inserted_row:
          log.info(f"Saved chunk of file id {file_id} from position {start_position}")
          return inserted_row[0]
        else:
          raise Exception("Insert into chunk table failed")

def read_chunks(chunk_ids: List[str]) -> List[ChunkData]:
    if len(chunk_ids) == 0:
        return []

    ids = tuple(chunk_ids)

    with get_conn().cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM chunk WHERE chunk_id IN %s", (ids,))
        rows = cursor.fetchall()

        return list(map(lambda r: ChunkData(**r), rows))

def read_chunks_of_file(file_id: int) -> List[ChunkData]:
    with get_conn().cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM chunk WHERE file_id = %s", (file_id,))
        rows = cursor.fetchall()
        return list(map(lambda r: ChunkData(**r), rows))
