import socket

s = socket.socket()
s.connect(("localhost", 8080))

s.settimeout(3)

try:
    data = s.recv(1024)
    print(b"Received data: {data}")
except socket.timeout:
    print("Read timeout...")

try:
    s.send(b"Ping after read timeout")
    print("Socket is still workable")
except socket.timeout as e:
    print(f"socket error after timeout {e}")

s.close()
