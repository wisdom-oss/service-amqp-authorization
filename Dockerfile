FROM python:3.10-alpine
RUN mkdir -p /opt/amqp-auth-service
COPY . /opt/amqp-auth-service
RUN python -m pip install -r /opt/amqp-auth-service/requirements.txt
WORKDIR /opt/amqp-auth-service
ENTRYPOINT ["python", "service.py"]
