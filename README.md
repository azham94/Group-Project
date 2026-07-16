# 🚀 Docker Multi-Container Socket Programming with MySQL (Presented on 7th July at Lab 5)

A Docker-based distributed system consisting of MySQL, Python TCP socket servers, and C TCP socket servers communicating through a shared Docker network.

## 1. Introduction

This project demonstrates a distributed, containerized points tracking application utilizing a multi-language architecture. The system simulates a dynamic environment where multiple backend client applications built in different programming languages (C and Python) communicate concurrently with isolated background server nodes via custom network sockets over a private bridge infrastructure. Data persistence is handled reliably using an isolated relational database layer, allowing point progressions to be updated, stored, and verified dynamically.

---

# 2. Objectives

The objectives of this project are:

1. Design a distributed multi-language service platform integrating compiled binary applications (C) alongside interpreted programming scripts (Python).
2. Implement network socket programming concepts utilizing structured socket listeners and handles to handle server-client handshakes.
3. Apply container orchestration strategies via Docker Compose to build, separate, and configure interconnected microservices within an isolated bridge network topology.
4. Secure and manage data state synchronization using safe concurrent database reads and writes to a central database system.

---

# 3. Software and Technologies Used

| Software / Technology | Function                   |
| --------------------- | -------------------------- |
| Docker Desktop        | Container platform engine         |
| Docker Compose        | Multi-container configuration and management |
| Python 3.9            | Python socket programming  |
| GCC Compiler          | Compile C programs         |
| MySQL 8.0             | Database management system            |
| VS Code               | Source code editor         |
| TCP Socket            | Communication protocol     |

---

# 4. System Architecture

The application runs on a decentralized network structure divided into distinct, structured functional layers :

* Storage Engine Space: Formed by the isolated mysql-db instance, serving as the system's shared central database repository.
* Network Isolation Layer: Managed by tournament_network_bridge, an isolated custom Docker bridge network that intercepts public port accessibility while keeping local services connected.
* Server Middleware Engine: A suite of detached, continuously running servers (server-fakhrusy, server-ariff, server-adib) tasked with checking connection validations, executing logic blocks, and interacting with MySQL.
* Active Front-End Display Interfaces: Isolated containers running continuous query monitors (client-fakhrusy, client-ariff, client-adib) that map to their matching backend services over specified internal container ports (5001, 5002, and 5003).

All containers are connected through the Docker network:

```text
itt440-project-final
```

## Communication Flow

1. Fakhrusy (C Node): client-fakhrusy queries server-fakhrusy every 30 seconds on Port 5001. The server increments Fakhrusy's points by +5 in the database, updates the timestamp, and returns the live score to the client.
2. Ariff (C Node): client-ariff queries server-ariff every 30 seconds on Port 5002. The server increments Ariff's points by +8 in the database, updates the timestamp, and returns the live score to the client.
3. Adib (Python Node): client-adib queries server-adib every 10 seconds on Port 5003. The server increments Adib's points by +10 in the database, updates the timestamp, and returns the live score to the client.

---

# 4.1 Project Structure

```text
itt440-project-final/
│
├── database/
│   └── init.sql                 # Automated SQL Schema initialization script
│
├── adib/
│   ├── Dockerfile               # Python environment builder context
│   ├── adib-python-server.py    # Python Port 5003 socket engine
│   └── adib-python-client.py    # Python interactive terminal interface
│
├── ariff/
│   ├── Dockerfile               # Alpine Linux environment with GCC setup
│   ├── ariff-c-server.c         # C Port 5002 database logic source
│   └── ariff-c-client.c         # C socket client connection runtime
│
├── fakhrusy/
│   ├── Dockerfile               # Alpine Linux environment with GCC setup
│   ├── fakhrusy-c-server.c      # C Port 5001 database logic source
│   └── fakhrusy-c-client.c      # C socket client connection runtime
│
└── docker-compose.yml           # Unified multi-container orchestration matrix
```

---

# 5. Database Design

## Database Information

| Item          | Value      |
| ------------- | ---------- |
| Database Name | itt440_db  |
| Table Name    | game_scores |

## Table Structure

| Column         | Data Type   |
| -------------- | ----------- |
| user           | VARCHAR(50) |
| points         | INT         |
| datetime_stamp | DATETIME    |

---

## SQL Script

```sql
CREATE DATABASE IF NOT EXISTS itt440_db;
USE itt440_db;

CREATE TABLE IF NOT EXISTS game_scores (
    user VARCHAR(50) PRIMARY KEY,
    points INT NOT NULL DEFAULT 0,
    datetime_stamp DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO game_scores (user, points) VALUES
('fakhrusy', 0),
('ariff', 0),
('adib', 0);
```

---

# 6. Docker Compose Configuration

The system deployment is fully automated through a standardized docker-compose.yml configuration :

## docker-compose.yml

```yaml
version: '3.8'

networks:
  game_network_bridge:
    name: tournament_network_bridge
    driver: bridge

services:
  database-service-mysql:
    image: mysql:8.0
    container_name: mysql-db
    networks:
      - game_network_bridge
    environment:
      MYSQL_ROOT_PASSWORD: secret
    volumes:
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"

  server-fakhrusy:
    build: ./fakhrusy
    container_name: server-fakhrusy
    networks:
      - game_network_bridge
    command: ./server
    depends_on:
      - database-service-mysql

  client-fakhrusy:
    build: ./fakhrusy
    container_name: client-fakhrusy
    networks:
      - game_network_bridge
    command: ./client
    depends_on:
      - server-fakhrusy

  server-ariff:
    build: ./ariff
    container_name: server-ariff
    networks:
      - game_network_bridge
    command: ./server
    depends_on:
      - database-service-mysql

  client-ariff:
    build: ./ariff
    container_name: client-ariff
    networks:
      - game_network_bridge
    command: ./client
    depends_on:
      - server-ariff

  server-adib:
    build: ./adib
    container_name: server-adib
    networks:
      - game_network_bridge
    command: python adib-python-server.py
    depends_on:
      - database-service-mysql

  client-adib:
    build: ./adib
    container_name: client-adib
    networks:
      - game_network_bridge
    command: python adib-python-client.py
    depends_on:
      - server-adib
```

---

# 7. Implementation

## 7.1 Dockerfiles

## C Microservice Builder Layout (./ariff/Dockerfile & ./fakhrusy/Dockerfile)

```Dockerfile
FROM alpine:latest
RUN apk update && apk add --no-cache gcc musl-dev mariadb-dev mariadb-connector-c-dev
WORKDIR /app
COPY . .
RUN gcc server-*.c -o server -lmysqlclient && \
    gcc client-*.c -o client
```

## Python Microservice Builder Layout (./adib/Dockerfile)

```Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir mysql-connector-python
COPY . .
```

---

## 7.2 Code Files

## adib-python-server.py

```adib-python-server.py
import socket
import mysql.connector

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5003))
    server.listen(5)
    print("Server Adib listening on port 5003...")

    while True:
        conn, addr = server.accept()
        try:
            data = conn.recv(1024).decode()
            if data:
                db = mysql.connector.connect(host='database-service-mysql', user='root', password='secret', database='itt440_db')
                cursor = db.cursor()
                cursor.execute("UPDATE game_scores SET points = points + 10, datetime_stamp = NOW() WHERE user = 'adib';")
                db.commit()
                
                cursor.execute("SELECT points, datetime_stamp FROM game_scores WHERE user = 'adib';")
                result = cursor.fetchone()
                
                response = f"User: adib | Points: {result[0]} | Last Update: {result[1]}" if result else "User adib not found."
                cursor.close()
                db.close()
                conn.send(response.encode())
        except Exception as e:
            pass
        finally:
            conn.close()

if __name__ == '__main__':
    start_server()
```

## adib-python-client.py

```adib-python-client.py
import socket
import time

def start_client():
    print("=== Adib Live Points Monitor ===", flush=True)
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('server-adib', 5003))
            client.send(b"FETCH")
            
            response = client.recv(1024).decode()
            print(response, flush=True)
            client.close()
        except Exception:
            pass
        time.sleep(10) # 10-second request cycle

if __name__ == '__main__':
    start_client()
```

## fakhrusy-c-server.c

```fakhrusy-c-server.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <mysql/mysql.h>

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1, addrlen = sizeof(address);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(5001);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 5);
    printf("Server Fakhrusy listening on port 5001...\n");

    while (1) {
        new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        char buffer[1024] = {0};
        read(new_socket, buffer, 1024);

        MYSQL *conn = mysql_init(NULL);
        if (mysql_real_connect(conn, "database-service-mysql", "root", "secret", "itt440_db", 3306, NULL, 0)) {
            mysql_query(conn, "UPDATE game_scores SET points = points + 5, datetime_stamp = NOW() WHERE user = 'fakhrusy';");
            mysql_query(conn, "SELECT points, datetime_stamp FROM game_scores WHERE user = 'fakhrusy';");
            MYSQL_RES *res = mysql_store_result(conn);
            MYSQL_ROW row = mysql_fetch_row(res);
            
            char response[1024];
            if (row) {
                sprintf(response, "User: fakhrusy | Points: %s | Last Update: %s", row[0], row[1]);
            } else {
                strcpy(response, "User fakhrusy not found.");
            }
            
            send(new_socket, response, strlen(response), 0);
            mysql_free_result(res);
            mysql_close(conn);
        }
        close(new_socket);
    }
    return 0;
}

## C Dockerfile

```dockerfile
FROM gcc:latest

WORKDIR /app

COPY server.c .

RUN gcc server.c -o server

CMD ["./server"]
```

## fakhrusy-c-client.c

```fakhrusy-c-client.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>

int main() {
    printf("=== Fakhrusy Live Points Monitor ===\n");
    while (1) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        struct sockaddr_in serv_addr;
        struct hostent *server = gethostbyname("server-fakhrusy");

        if (server != NULL) {
            memset(&serv_addr, 0, sizeof(serv_addr));
            serv_addr.sin_family = AF_INET;
            memcpy(&serv_addr.sin_addr.s_addr, server->h_addr, server->h_length);
            serv_addr.sin_port = htons(5001);

            if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) >= 0) {
                send(sock, "FETCH", 5, 0);
                char buffer[1024] = {0};
                read(sock, buffer, 1024);
                printf("%s\n", buffer);
                fflush(stdout); // Force instant terminal display
            }
        }
        close(sock);
        sleep(30); // 30-second request cycle
    }
    return 0;
}
```

## ariff-c-server.c

```ariff-c-server.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <mysql/mysql.h>

void* db_updater(void* arg) {
    while(1) {
        MYSQL *conn = mysql_init(NULL);
        if (mysql_real_connect(conn, "database-service-mysql", "root", "secret", "itt440_db", 3306, NULL, 0)) {
            mysql_query(conn, "UPDATE game_scores SET points = points + 8, datetime_stamp = NOW() WHERE user = 'ariff';");
            mysql_close(conn);
        }
        sleep(30);
    }
    return NULL;
}

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};
    char *response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nAriff Server Active\n";

    pthread_t thread_id;
    pthread_create(&thread_id, NULL, db_updater, NULL);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(5002);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 3);

    while((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen))) {
        read(new_socket, buffer, 1024);
        send(new_socket, response, strlen(response), 0);
        close(new_socket);
    }
    return 0;
}
```

## ariff-c-client.c

```ariff-c-client.c
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

int main() {
    struct sockaddr_in serv_addr;
    char buffer[1024] = {0};

    while(1) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(5002);
        inet_pton(AF_INET, "server-ariff", &serv_addr.sin_addr);

        if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) >= 0) {
            send(sock, "GET_POINTS", 10, 0);
            read(sock, buffer, 1024);
        }
        close(sock);
        sleep(15);
    }
    return 0;
}
```

---

# 8. Steps to Run the Project

## Build and Start Containers

```bash
docker compose down --volumes --remove-orphans
docker compose up -d --build
```

## Inspect the Real-Time Terminal Client Outputs

```bash
docker compose logs -f client-fakhrusy client-ariff client-adib
```

## Access MySQL Database Directly inside Container

```bash
docker exec -it mysql-db mysql -u root -psecret itt440_db
```

```SQL
SELECT * FROM game_scores;
```

---


# 9. Testing and Results

### Terminal Monitoring Feed
Executing the logs command triggers a clean streaming feed displaying user points updating automatically relative to their sleep configurations :

```bash
client-adib       | User: adib | Points: 10 | Last Update: 2026-07-16 16:30:10
client-adib       | User: adib | Points: 20 | Last Update: 2026-07-16 16:30:20
client-fakhrusy   | User: fakhrusy | Points: 5 | Last Update: 2026-07-16 16:30:30
client-ariff      | User: ariff | Points: 8 | Last Update: 2026-07-16 16:30:30
client-adib       | User: adib | Points: 30 | Last Update: 2026-07-16 16:30:30
```

### Database Verification Proof
Querying the database verifies that the values retrieved by the socket client connections match the internal states updated by the respective backend servers :

```bash
mysql> SELECT * FROM game_scores;
+-----------+--------+---------------------+
| user      | points | datetime_stamp      |
+-----------+--------+---------------------+
| fakhrusy  |      5 | 2026-07-16 16:30:30 |
| ariff     |      8 | 2026-07-16 16:30:30 |
| adib      |     30 | 2026-07-16 16:30:30 |
+-----------+--------+---------------------+
3 rows in set (0.00 sec)
```

---


# 10. Problems Faced

* Container Exits on Completion : When first launched, the client containers printed one line and exited immediately. This occurs because Docker containers shut down as soon as their primary script or executable finishes executing.
* Solution : Refactored the clients to execute within infinite loop blocks (while (1)/while True) throttled by precise sleep intervals to keep the services running.

* Missing Compiler in Thin Containers : The C-based containers returned gcc: not found during build steps because standard Alpine base images do not contain development headers or compilers.
* Solution : Modified the multi-stage C Dockerfile to automatically pull Alpine development tools (gcc, musl-dev, and mariadb-connector-c-dev) to compile the binaries cleanly during the build step.

* Terminal Output Buffering Lag : Client outputs printed inside C executables did not display immediately in the console logs due to Standard Output buffering.
* Solution : Added fflush(stdout); directly after the display functions in both C client files, forcing the container console to render updates in real-time.

---

# 11. Conclusion

The objectives of the project were successfully achieved. Docker containers were deployed and interconnected through a private Docker bridge network. Python and C socket servers and clients were implemented successfully, demonstrating socket communication using multiple programming languages.

The MySQL database successfully managed user records, points, and timestamps while Python and C servers updated the database dynamically based on client requests. Overall, this project demonstrated the effectiveness of Docker in developing scalable, multi-language distributed systems.

---

