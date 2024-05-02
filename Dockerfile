FROM python:3.8.0

WORKDIR /app

RUN pip3 install minio==7.2.3 protobuf==3.20.3 grpcio==1.60.0 grpcio-health-checking==1.48.2
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 51001

CMD [ "python3", "manage.py"]
