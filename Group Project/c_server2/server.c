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
            mysql_query(conn, "UPDATE game_scores SET points = points + 5, datetime_stamp = NOW() WHERE user = 'fakhrusy';");
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
    char *response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nFakhrusy Server Active\n";

    pthread_t thread_id;
    pthread_create(&thread_id, NULL, db_updater, NULL);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(5001);

    bind(server_fd, (struct sockaddr *)&address, sizeof(address));
    listen(server_fd, 3);

    while((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen))) {
        read(new_socket, buffer, 1024);
        send(new_socket, response, strlen(response), 0);
        close(new_socket);
    }
    return 0;
}
