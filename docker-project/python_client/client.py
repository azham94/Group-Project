import socket
import time

time.sleep(40)

HOST = "python_server"
PORT = 5000

client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)

client.connect((HOST, PORT))

data = client.recv(1024)

print("Latest Point:", data.decode())

client.close()