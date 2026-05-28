import socket
import time

server = socket.socket()
server.bind(("localhost", 8080))
server.listen(1)

print("Server is listening on port 8080")

conn, addr = server.accept()
print(f"Client connected, {addr}")

time.sleep(10)
conn.sendall(b"Hello, client from server.")
conn.close()
