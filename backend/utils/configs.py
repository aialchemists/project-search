import json
from dataclasses import dataclass

_file = open('./configs.json')
configs = json.load(_file)

@dataclass
class DBConfigs:
    host: str
    port: int
    user: str
    password: str
    dbname: str

    def get_dsn(self):
        return  f"dbname='{self.dbname}' user='{self.user}' host='{self.host}' port='{self.port}' password='{self.password}'"

db_configs = DBConfigs(**configs["db"])

@dataclass
class ChunkConfigs:
    max_length: int
    degree: int

chunk_configs = ChunkConfigs(**configs["chunk"])

@dataclass
class EmbeddingConfigs:
    model: str

embedding_configs = EmbeddingConfigs(**configs["embedding"])
