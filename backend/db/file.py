from typing import Optional
from dataclasses import dataclass
from utils.logger import log

from . import get_conn
from psycopg2.extras import RealDictCursor

from typing import Union

@dataclass
class FileData:
    file_type: str
    file_path: str
    content: str
    file_id: Optional[int] = None

def save_file(data: FileData) -> int:
    with get_conn().cursor() as cursor:
        cursor.execute("INSERT INTO file (file_type, file_path, content) VALUES (%s,%s,%s) RETURNING *", (data.file_type, data.file_path, data.content))
        get_conn().commit()

        inserted_row = cursor.fetchone()
        if inserted_row:
          log.info(f"Saved details of file {data.file_path}")
          return inserted_row[0]
        else:
          raise Exception("Insert into file table failed")

def read_file(file_id: int) -> Union[FileData, None]:
    with get_conn().cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM file WHERE file_id = %s", (file_id,))
        row = cursor.fetchone()
        return FileData(**row) if row else None
