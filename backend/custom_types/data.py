from typing import Optional
from dataclasses import dataclass

# TODO: Use pydantic instead of dataclass
@dataclass
class FileData:
    file_id: Optional[int]
    file_path: str
    content: str

@dataclass
class Chunk:
   chunk_id: int
   file_id: int
   chunk_text: str
   start_position: int
   length: int
