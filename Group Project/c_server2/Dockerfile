FROM ubuntu:22.04
RUN apt-get update && apt-get install -y gcc libmysqlclient-dev
WORKDIR /app
COPY . .
RUN gcc fakhrusy-c-server.c -o server -lmysqlclient -lpthread
RUN gcc fakhrusy-c-client.c -o client
