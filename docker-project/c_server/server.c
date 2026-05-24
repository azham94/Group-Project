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