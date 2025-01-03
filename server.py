import logging
import sys
from concurrent import futures

import grpc

sys.path.append("generated_protos")
from generated_protos import hello_pb2_grpc
from grpc_services.hello_service import HelloService


def serve():
    port = "6565"
    logging.info("Server is listening at port %s", port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
