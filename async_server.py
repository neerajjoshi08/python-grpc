import logging
from os import getenv

import grpc


def serve() -> None:

    # Here, we need to setup for gRPC
    grpc.aio.server()


if __name__ == "__main__":
    # We need to set the log level as INFO but at it can be tweaked using env variable
    # Also we can dump the logs into the file
    log_level = getenv("LOG_LEVEL", logging.INFO)
    logging.basicConfig(level=log_level)
    serve()
