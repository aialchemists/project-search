import json
import grpc
from concurrent import futures

from .action_pb2_grpc import ActionStub
from .action_pb2 import Request, Response

class ARPCClient():
    url: str

    def __init__(self, url: str):
        self.url = url
        # TODO: Convert to async
        self.channel = grpc.insecure_channel(url)

    def call(self, action_name: str, data: dict) -> dict:
        stub = ActionStub(self.channel)
        request: Request = Request(action_name=action_name, data=json.dumps(data))
        response: Response = stub.call(request)
        resp_data = json.loads(response.data)
        return resp_data
