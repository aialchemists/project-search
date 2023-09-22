import json
import grpc
from concurrent import futures

from .action_pb2_grpc import ActionStub
from .action_pb2 import Request, Response

class ARPCClient():
    url: str

    def __init__(self, url: str):
        self.url = url
        self.channel = grpc.aio.insecure_channel(url)

    def __enter__(self):
        return self

    async def __exit__(self, exc_type, exc_value, traceback):
        await self.channel.close()

    async def call(self, action_name: str, data: dict) -> dict:
        stub = ActionStub(self.channel)
        request: Request = Request(action_name=action_name, data=json.dumps(data))
        response: Response = await stub.call(request)
        resp_data = json.loads(response.data)
        return resp_data
