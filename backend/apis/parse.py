from utils.action_rpc.client import ARPCClientSync
from db.file import FileData

client: ARPCClientSync

def init():
    global client
    client = ARPCClientSync("localhost:50052")

def parse_file(file_path: str) -> tuple[FileData, dict]:
    resp = client.call("parse", {
      "file_path": file_path
    })
    return FileData(**resp["file_data"]), resp["metadata"]
