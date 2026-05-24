import socket
import time
import mysql.connector
from threading import Thread

HOST = '0.0.0.0'
PORT = 5000

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

        sql = """
        UPDATE scoreboard
        SET points=%s,
            datetime_stamp=NOW()
        WHERE user='python_user'
        """

        cursor.execute(sql, (points,))
        db.commit()

        print("Database Updated")

        time.sleep(30)

Thread(target=update_db, daemon=True).start()

server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen(5)

print("Python Server Running...")

while True:

    client, addr = server.accept()

    cursor.execute("""
    SELECT points
    FROM scoreboard
    WHERE user='python_user'
    """)

    result = cursor.fetchone()

    client.send(str(result[0]).encode())

    client.close()