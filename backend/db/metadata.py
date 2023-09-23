from dataclasses import dataclass

from psycopg2.extras import RealDictCursor
from typing import Union

from . import get_conn

@dataclass
class Metadata:
    file_id: int
    meta_key: str
    meta_value: str

def save_meta() -> int:
    return 0

def read_meta(file_id: int) -> Union[Metadata, None]:
    return None
