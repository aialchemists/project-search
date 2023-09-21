from dataclasses import dataclass

# TODO: Use pydantic instead of dataclass
@dataclass
class FileData:
    file_path: str
    content: str
    metadata: dict
