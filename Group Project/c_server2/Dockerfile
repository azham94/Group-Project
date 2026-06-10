FROM gcc:latest

WORKDIR /app

COPY server.c .

RUN gcc server.c -o server

CMD ["./server"]