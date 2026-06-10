import socket
import time
import mysql.connector

from threading import Thread
from datetime import datetime
from zoneinfo import ZoneInfo

HOST = "0.0.0.0"
PORT = 5002

time.sleep(20)

db = mysql.connector.connect(
    host="mysql_db",
    user="root",
    password="root",
    database="projectdb"
)

cursor = db.cursor()

points = 0

def update_db():
    global points

    while True:

        points += 10

        current_time = datetime.now(
            ZoneInfo("Europe/London")
        )

        cursor.execute("""
        UPDATE scoreboard
        SET points=%s,
            datetime_stamp=%s
        WHERE user='python_user2'
        """, (points, current_time))

        db.commit()

        print(
            f"python_user2 updated | "
            f"{current_time}"
        )

        time.sleep(30)

Thread(target=update_db, daemon=True).start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(5)

print("Python Server2 Running")

while True:

    client, address = server.accept()

    cursor.execute("""
    SELECT points
    FROM scoreboard
    WHERE user='python_user2'
    """)

    result = cursor.fetchone()

    client.send(str(result[0]).encode())

    client.close()