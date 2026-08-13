FROM ubuntu:22.04
RUN apt-get update && apt-get install -y gcc libmysqlclient-dev
WORKDIR /app
COPY . .
RUN gcc ariff-c-server.c -o server -lmysqlclient -lpthread
RUN gcc ariff-c-client.c -o client
