import asyncio
import grpc
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.grpc import GrpcAioInstrumentorServer
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor
from prometheus_client import start_http_server

from py_async_grpc_prometheus.prometheus_async_server_interceptor import (
    PromAsyncServerInterceptor,
)

import helloworld_pb2
import helloworld_pb2_grpc

# Your proto imports
# import your_service_pb2
# import your_service_pb2_grpc

# Set up Prometheus metrics
prometheus_reader = PrometheusMetricReader()
meter_provider = MeterProvider(metric_readers=[prometheus_reader])
metrics.set_meter_provider(meter_provider)

meter = metrics.get_meter(__name__)
counter = meter.create_counter("test_counter")

# Instrument gRPC server
grpc_server_instrumentor = AsyncioInstrumentor()
grpc_server_instrumentor.instrument()


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    """Example bidirectional streaming service"""

    async def SayHelloBidiStream(self, request_iterator, context):
        """
        Bidi streaming RPC - metrics are automatically collected for:
        - Stream duration
        - Number of messages sent/received
        - Stream status
        """
        counter.add(1)
        async for request in request_iterator:
            # Process incoming message
            print(f"Received: {request}")

            # Send response back
            # response = your_service_pb2.YourResponse(...)
            # yield response

            # Metrics are automatically tracked:
            # - rpc.server.duration (total stream duration)
            # - rpc.server.requests_per_rpc (messages received)
            # - rpc.server.responses_per_rpc (messages sent)
            yield helloworld_pb2.HelloReply(message=f"Hello message")


async def serve():
    # Start Prometheus HTTP server for metrics
    start_http_server(port=8000, addr="0.0.0.0")
    print("Prometheus metrics server started on :8000")

    # Create gRPC server
    server = grpc.aio.server(
        interceptors=(PromAsyncServerInterceptor(),),
        options=[
            ("grpc.max_send_message_length", 50 * 1024 * 1024),
            ("grpc.max_receive_message_length", 50 * 1024 * 1024),
        ],
    )

    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # Add your service
    # your_service_pb2_grpc.add_YourServiceServicer_to_server(
    #     YourBidiService(), server
    # )

    server.add_insecure_port("[::]:50051")
    await server.start()
    print("gRPC Server started on :50051")
    print("Metrics available at http://localhost:8000/metrics")

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        await server.stop(grace=5)


if __name__ == "__main__":
    asyncio.run(serve())
