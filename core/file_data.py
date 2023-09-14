from dataclasses import dataclass

@dataclass
class FileData:
    file_path: str
    content: str
    metadata: dict
