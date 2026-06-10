FROM python:3.9

WORKDIR /app

ENV TZ=Europe/London

COPY server.py .

RUN pip install mysql-connector-python

CMD ["python", "server.py"]