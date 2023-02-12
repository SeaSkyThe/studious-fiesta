# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine

WORKDIR /src

COPY requirements.txt /src
RUN pip3 install -r requirements.txt

COPY ./src /src

ENTRYPOINT ["python3"]

CMD ["app.py"]

