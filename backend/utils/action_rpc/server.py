import json
import grpc

from typing import Dict, Callable

from utils.logger import log

from .action_pb2_grpc import ActionServicer, add_ActionServicer_to_server
from .action_pb2 import Request, Response

NUM_SECS_TO_WAIT_ON_STOP = 3

Handler = Callable[[dict], dict]
ActionsDict = Dict[str, Handler]

class Action(ActionServicer):
    actions: ActionsDict

    def __init__(self, actions: ActionsDict):
      self.actions = actions

    async def call(self, request: Request, context) -> Response:
        action_handler = self.actions[request.action_name]
        data = json.loads(request.data)
        if action_handler:
            data = action_handler(data)
            return Response(data=json.dumps(data))
        else:
            log.error(f"Action not registered {request.action_name}")
            return Response(data=None)

class ARPCServer():
    port: str
    actions: ActionsDict

    def __init__(self, port: str):
        self.port = port
        self.actions = {}
        self.server = self._create_server()

    def _create_server(self):
        server = grpc.aio.server()
        add_ActionServicer_to_server(Action(self.actions), server)
        listen_addr = f"[::]:{self.port}"
        server.add_insecure_port(listen_addr)
        return server

    async def start(self):
        await self.server.start()
        log.info("aRPC Server started, listening on " + self.port)
        await self.server.wait_for_termination()

    async def stop(self):
        await self.server.stop(NUM_SECS_TO_WAIT_ON_STOP)

    def register_action(self, action_name: str, handler: Handler):
        self.actions[action_name] = handler

    def remove_action(self, action_name: str):
        del self.actions[action_name]
