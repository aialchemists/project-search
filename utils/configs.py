import json
from dataclasses import dataclass

_file = open('./configs.json')
_data = json.load(_file)

@dataclass
class DBConfigs:
    host: str
    port: int
    user: str
    password: str
    dbname: str

    def get_dsn(self):
        return  f"dbname='{self.dbname}' user='{self.user}' host='{self.host}' port='{self.port}' password='{self.password}'"

db_configs = DBConfigs(**_data["db"])
