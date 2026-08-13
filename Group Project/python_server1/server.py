import socket
import threading
import time
import mysql.connector

def update_db():
    while True:
        try:
            conn = mysql.connector.connect(host="database-service-mysql", user="root", password="secret", database="itt440_db")
            cursor = conn.cursor()
            cursor.execute("UPDATE game_scores SET points = points + 10, datetime_stamp = NOW() WHERE user = 'adib'")
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            pass
        time.sleep(30)

threading.Thread(target=update_db, daemon=True).start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5003))
server.listen(5)

while True:
    client_sock, addr = server.accept()
    data = client_sock.recv(1024)
    client_sock.send(b"HTTP/1.1 200 OK\n\nAdib Server Active\n")
    client_sock.close()
