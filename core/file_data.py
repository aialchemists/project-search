from dataclasses import dataclass

@dataclass
class FileData:
    id: str
    file_name: str
    content: str
    metadata: dict