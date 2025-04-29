FROM python:3.12-alpine

# Install system dependencies needed for compiling cryptography and mysqlclient
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    mariadb-dev \
    pkgconfig

WORKDIR /code

COPY ./boot/docker-run.sh /opt/run.sh
RUN chmod +x /opt/run.sh

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code

# Tomo el archivo .env_to_docker como env
RUN rm -f ./code/.env
RUN mv .env_to_docker .env

CMD ["/opt/run.sh"]