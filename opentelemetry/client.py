import asyncio
import grpc
import helloworld_pb2
import helloworld_pb2_grpc


async def request_generator():
    for msg in ["one", "two", "three"]:
        print(f"Sending: {msg}")
        yield helloworld_pb2.HelloRequest(name=msg)


async def run():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        responses = stub.SayHelloBidiStream(request_generator())

        async for response in responses:
            print(f"Received: {response.message}")


asyncio.run(run())
