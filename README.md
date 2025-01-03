## Hello world python grpc

## Set up python virtual env
```bash
python -m venv .venv
source .venv/bin/active
python -m pip install --upgrade pip
```

## Activate virtual env if already exists
```bash
source .venv/bin/activate
```

## Deactivate from the current virtual env
```bash
deactivate
```

## Install dependencies
```bash
python -m pip install -r requirements.txt
```

## How to generate proto files
```bash
python -m grpc_tools.protoc \
  --proto_path=protos \
  --python_out=generated_protos \
  --grpc_python_out=generated_protos \
  --pyi_out=generated_protos \
  protos/*.proto
```

## gRPC UI
```bash
grpcui -plaintext -import-path=<protos-path> -proto=<.proto> localhost:<server-port>

# Example:
grpcui -plaintext -import-path=protos -proto=hello.proto localhost:6565
```