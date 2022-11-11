# echo-client.py

import socket
import time

HOST = "172.16.31.82"  # The server's hostname or IP address
PORT = 65432  # The port used by the server


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    time.sleep(0.2)
    data = s.recv(1024)
    print(f"Received {data!r}")
