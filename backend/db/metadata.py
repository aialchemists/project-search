from dataclasses import dataclass

from psycopg2.extras import RealDictCursor
from typing import List

from . import get_conn

@dataclass
class Metadata:
    file_id: int
    meta_key: str
    meta_value: str

def save_meta(file_id, metadata):
    with get_conn().cursor() as cursor:
        # Inserting metadata into the 'metadata' table
        metadata_entries = [
            ('file_type', metadata['file_format']),
            ('year', metadata['year']),
            ('author', metadata['author']),
            ('language', metadata['language'])
        ]

        cursor.executemany("INSERT INTO metadata (file_id, meta_key, meta_value) VALUES (%s, %s, %s)",
                           [(file_id, key, value) for key, value in metadata_entries])
        get_conn().commit()

def read_meta(file_ids) -> List[Metadata]:
    ids = tuple(file_ids)

    with get_conn().cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM metadata WHERE file_id IN %s", (ids,))
        rows = cursor.fetchall()
        return list(map(lambda r: Metadata(**r), rows))
