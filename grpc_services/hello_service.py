import logging

import grpc
from google.protobuf.json_format import MessageToJson

from generated_protos import hello_pb2_grpc, hello_pb2


class HelloService(hello_pb2_grpc.HelloServiceServicer):
    def SayHello(
            self,
            request: hello_pb2.HelloRequest,
            context: grpc.ServicerContext
    ):
        logging.info("Received request, %s", MessageToJson(request))
        return hello_pb2.HelloResponse(message=f"Hello, {request.name}")
