import logging
import sys
from concurrent import futures

import grpc
import redis

sys.path.append("generated_protos")
from generated_protos import hello_pb2_grpc
from grpc_services.hello_service import HelloService


class RedisConnection:
    def __init__(self):
        pass

    def connect(self, host: str, port: int):
        self.r = redis.Redis(host, port, db=0)
        # redis.ConnectionPoPol()

    def set(self, key: str, value: str):
        self.r.set(key, value)

    def get(self, key: str) -> str:
        return self.r.get(key)


def redis_driver():
    redis_connection = RedisConnection()
    redis_connection.connect(host="localhost", port=6379)
    for i in range(10):
        redis_connection.set(f"Hello:{i}", "World:{i`}")
    value = redis_connection.get("Hello")
    print(f"Value received from Redis: {value}")


def serve():
    port = "50051"
    logging.info("Server is listening at port %s", port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServiceServicer_to_server(HelloService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # redis_driver()
    serve()
