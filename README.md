# ITT440: Group Project - Docker Containerized Socket Programming System
**Course:** ITT440 - Network Programming  
**Group:** NBCS2555B   
**Name:** MOHD SYAHRUL AZHAM BIN MOHD SHAFIE  
**Student ID:** 2024358831   
**Name:** AHMAD HAFIY BIN MOHD AZRI  
**Student ID:** 2024129101 
**Name:** MUHD AMIR ASYRAF BIN MOHD TAHA  
**Student ID:** 2025456114  
**Lecturer:** Sir Shahadan Bin Saad  
<br />

# 1. Introduction <br />
This project is developed for the ITT440 Network Programming course. The objective of this project is to implement a Docker-based containerized networking system using both Python and C socket programming. <br />
The project contains three main types of containers:<br />
•	Database Container <br />
•	Socket Server Container <br />
•	Socket Client Container <br />
<br />
Docker technology is used to deploy and manage all containers inside the same network environment so that they can communicate with each other. <br />
The project also demonstrates: <br />
•	TCP socket communication <br />
•	Docker networking <br />
•	Database integration <br />
•	Python socket programming <br />
•	C socket programming <br />
•	Client-server communication <br />
<br />

# 2. Objectives <br />
The objectives of this project are: <br />
•	To deploy multiple Docker containers. <br />
•	To implement TCP socket communication. <br />
•	To use MySQL database container. <br />
•	To implement Python socket programming. <br />
•	To implement C socket programming. <br />
•	To allow communication between containers in the same Docker network. <br />
•	To update database records every 30 seconds. <br />
•	To allow client containers to request latest points from server containers. <br />
 <br />

# 3. Software and Technologies Used

| Software / | Technology	Function |
|---------------------|------------------------------|
| Docker Desktop |	Container platform |
| Docker Compose |	Multi-container management |
| Python 3.9 | Python socket programming |
| GCC Compiler	| Compile C programs |
| MySQL 5.7	| Database server |
| VS Code	| Source code editor |
| TCP Socket	| Communication protocol |
 <br />

# 4. System Architecture

The system consists of five containers: <br />
•		MySQL Database Container <br />
•		Python Server Container <br />
•		Python Client Container <br />
•		C Server Container <br />
•		C Client Container <br />
 <br />
All containers are connected using the same Docker network called: <br />
    
    project_network
Communication flow: <br />
•	Python server updates database every 30 seconds. <br />
•	Python client requests latest points from Python server. <br />
•	C server sends points to C client. <br />
•	MySQL stores user, points, and timestamp data. <br />
 <br />

# 6.	Folder Structure
<img width="458" height="583" alt="image" src="https://github.com/user-attachments/assets/43ffaacb-9d21-4d9e-a26a-c2da0449befc" />

## 6.1.  Database Design

| Database Name: |	projectdb |
|---------------------|------------------------------|
| Table Name: |	scoreboard |

## 6.2. Table structure:

| Column |	Data Type |
|---------------------|------------------------------|
| user |	VARCHAR(50) |
| points |	INT |
| datetime_stamp |	DATETIME |

## 6.3. SQL code used:

    CREATE DATABASE projectdb;

    USE projectdb;
    
    CREATE TABLE scoreboard (
            user VARCHAR(50) PRIMARY KEY,
            points INT,
            datetime_stamp DATETIME
    );

    INSERT INTO scoreboard VALUES
    ('python_user', 0, NOW()),
    ('c_user', 0, NOW());

# 7. Docker Compose Configuration

Docker Compose is used to manage all containers in one configuration file. <br />
The docker-compose.yml file is responsible for: <br />
•	Building containers <br />
•	Creating Docker network <br />
•	Mapping ports <br />
•	Starting services automatically <br />
•	Managing dependencies between containers <br />
 <br />
## 7.1 Docker Compose configuration:
    version: '3'

    services:

      mysql_db:

    image: mysql:5.7

    container_name: mysql_db

    restart: always

    environment:
      MYSQL_ROOT_PASSWORD: root
      TZ: Asia/Kuala_Lumpur

    ports:
      - "3306:3306"

    volumes:
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql

    networks:
      - project_network

      python_server:

    build: ./python_server

    container_name: python_server

    depends_on:
      - mysql_db

    ports:
      - "5000:5000"

    networks:
      - project_network

      python_client:

    build: ./python_client

    container_name: python_client

    depends_on:
      - python_server

    networks:
      - project_network

      c_server:

    build: ./c_server

    container_name: c_server

    ports:
      - "6000:6000"

    networks:
      - project_network

      c_client:
    build: ./c_client
    container_name: c_client
    depends_on:
      - c_server
    networks:
      - project_network
    networks:
      project_network:
# 8. Python Server Implementation

The Python server acts as a TCP socket server. <br />
Functions of Python server: <br />
•	Connect to MySQL database <br />
•	Update database every 30 seconds <br />
•	Increase points value automatically <br />
•	Send latest points to client container <br />
 <br />
 ## 8.1 Python server code:
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
# 9. Python Client Implementation

The Python client connects to the Python server and requests the latest points. <br />
 
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
# 10. C Server Implementation

The C server acts as another TCP socket server. <br />
Functions of C server: <br />
•	Accept client connections <br />
•	Send points value to C client <br />

## 10.1. C server code:

    #include <stdio.h>
    #include <string.h>
    #include <unistd.h>
    #include <arpa/inet.h>
    int main() {
    int server_fd, client_socket;
    struct sockaddr_in server_addr;
    char message[] = "200";
    server_fd = socket(AF_INET,
    SOCK_STREAM,
    0);
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(6000);
    server_addr.sin_addr.s_addr = INADDR_ANY;
    bind(server_fd,
    (struct sockaddr*)&server_addr,
    sizeof(server_addr));
    listen(server_fd, 5);
    printf("C Server Running...\n");
    while(1) {
    client_socket = accept(server_fd,
    NULL,
    NULL);
    send(client_socket,
    message,
    strlen(message),
    0);
    printf("Point Sent To Client\n");
    close(client_socket);
    }
    return 0;
    }

# 11. C Client Implementation

The C client connects to the C server and receives latest points. <br />

## 11.1. C client code:

    #include <stdio.h>
    #include <string.h>
    #include <unistd.h>
    #include <netdb.h>
    #include <arpa/inet.h>

    int main() {

      int sock;
      struct sockaddr_in server_addr;
      struct hostent *host;
      char buffer[1024] = {0};
      host = gethostbyname("c_server");
      sock = socket(AF_INET, SOCK_STREAM, 0);
      server_addr.sin_family = AF_INET;
      server_addr.sin_port = htons(6000);
      memcpy(&server_addr.sin_addr, host->h_addr, host->h_length); connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr));
      read(sock, buffer, 1024);
      printf("Latest Point: %s\n", buffer);
      close(sock);

      return 0;
    }

# 12. Dockerfiles

## 12.1. Python Server Dockerfile
    FROM python:3.9
    WORKDIR /app
    ENV TZ=Asia/Kuala_Lumpur
    COPY server.py .
    RUN pip install mysql-connector-python
    CMD ["python", "server.py"]

## 12.2. Python Client Dockerfile
    FROM python:3.9
    WORKDIR /app
    COPY client.py .
    CMD ["python", "client.py"]

## 12.3. C Server Dockerfile
    FROM gcc:latest
    WORKDIR /app
    COPY server.c .
    RUN gcc server.c -o server
    CMD ["./server"]

## 12.4. C Client Dockerfile
    FROM gcc:latest
    WORKDIR /app
    COPY client.c .
    RUN gcc client.c -o client
    CMD ["./client"]

# 13. Steps to Run the Project

## 13.1. Build and Start Containers
    docker compose up --build

## 13.2. Check Running Containers
    docker ps

## 13.3. Enter MySQL Container
    docker exec -it mysql_db mysql -u root -p

## 13.4. Password:
    root
## 13.5. Check Database Records
    USE projectdb;

    SELECT * FROM scoreboard;


## 13.6. Stop Containers
    docker compose down

# 14. Results and Output

## 14.1. Build and Start Containers
    docker compose up --build
    
<img width="975" height="171" alt="image" src="https://github.com/user-attachments/assets/9d82f93d-c992-4eec-8b1e-03daed57f621" />

## 14.2. Check Running Containers
    docker ps

<img width="975" height="510" alt="image" src="https://github.com/user-attachments/assets/1ff6776d-426e-4417-aef4-ec06646c25b6" />

<img width="975" height="546" alt="image" src="https://github.com/user-attachments/assets/ee2d0d80-ce14-491a-a74f-9584cef16304" />



<img width="975" height="320" alt="image" src="https://github.com/user-attachments/assets/db303c93-4d4e-45db-903e-f2236f2b2ebe" />

## 14.3. Enter MySQL Container
    docker exec -it mysql_db mysql -u root -p

<img width="975" height="503" alt="image" src="https://github.com/user-attachments/assets/965158df-15eb-42e2-810f-4450d19aa73c" />

## 14.4. Password:
    root

<img width="624" height="176" alt="image" src="https://github.com/user-attachments/assets/d745532e-f05b-4d0f-91a0-bcbe36db7d20" />

## 14.5. Check Database Records
    USE projectdb;

    SELECT * FROM scoreboard;

<img width="975" height="564" alt="image" src="https://github.com/user-attachments/assets/4dd6bf3e-03bf-4e79-a192-b682b20f0563" />

## 13.6. Stop Containers
    docker compose down

<img width="975" height="290" alt="image" src="https://github.com/user-attachments/assets/8220e630-4f79-4a26-806b-086f5e41c8a4" />



# 15. Discussion

•	This project successfully demonstrates the implementation of Docker container technology integrated with socket programming. <br />
•	The use of Docker containers simplifies deployment and allows communication between multiple services in the same virtual network. <br />
•	The Python server successfully updates the MySQL database every 30 seconds while the clients are able to request the latest points from the servers. <br />
•	The project also demonstrates interoperability between different programming languages such as Python and C within Docker containers. <br />
•	Timezone configuration using Asia/Kuala_Lumpur (GMT+8) ensures that timestamps are synchronized with Malaysia local time. <br />

# 16. Problems Faced

Some problems encountered during the project: <br />

| Problem |	Solution |
|---------------------|------------------------------|
| MySQL container not ready |	Added time.sleep() delay |
| Containers cannot communicate |	Connected all containers to same Docker network |
| Docker compose file error |	Corrected YAML indentation |
| C client cannot connect using localhost |	Used Docker hostname instead |
| Timezone mismatch |	Configured Asia/Kuala_Lumpur timez |


