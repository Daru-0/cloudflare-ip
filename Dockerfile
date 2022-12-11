FROM python:3.7-alpine3.15

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY src/ .

CMD [ "python3", "main.py" ]
