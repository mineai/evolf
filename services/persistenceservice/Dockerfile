FROM python:3.7.6-stretch

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]

CMD ["persistence_server.py"]