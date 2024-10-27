FROM python:3.10

RUN mkdir -p /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags`
# RUN export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs`

COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install mysqlclient

COPY . .

EXPOSE 8000

WORKDIR /app
