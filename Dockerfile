FROM mysql:5.7

RUN apt-get update \
    && apt-get install -y python3 python3-pip

WORKDIR /db-server

COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY ./docker_init.sh /docker-entrypoint-initdb.d/docker_init.sh
RUN chmod +x /docker-entrypoint-initdb.d/docker_init.sh

ENV MYSQL_ROOT_PASSWORD 123456

COPY . .

EXPOSE 3306
