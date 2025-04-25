FROM python:3.12-alpine

WORKDIR /code

COPY ./boot/docker-run.sh /opt/run.sh
RUN chmod +x /opt/run.sh

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code

# Tomo el archivo .env_to_docker como env
RUN rm -f /code.env
RUN mv /code.env_to_docker /code.env


CMD ["/opt/run.sh"]