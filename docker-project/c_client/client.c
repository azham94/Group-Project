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

    sock = socket(AF_INET,
                  SOCK_STREAM,
                  0);

    server_addr.sin_family = AF_INET;

    server_addr.sin_port = htons(6000);

    memcpy(&server_addr.sin_addr,
           host->h_addr,
           host->h_length);

    connect(sock,
            (struct sockaddr*)&server_addr,
            sizeof(server_addr));

    read(sock, buffer, 1024);

    printf("Latest Point: %s\n", buffer);

    close(sock);

    return 0;
}