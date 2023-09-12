from dataclasses import dataclass

@dataclass
class FileData:
    id: str
    file_path: str
    content: str
    metadata: dict