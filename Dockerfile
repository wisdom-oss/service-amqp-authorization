FROM python:3.10-alpine
WORKDIR /service
COPY . /service
RUN python -m pip install -r /service/requirements.txt
ENTRYPOINT ["python", "service.py"]
