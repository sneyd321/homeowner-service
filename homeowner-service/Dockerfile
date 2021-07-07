FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install uwsgi

COPY . .

ENV FLASK_APP=app

CMD [ "uwsgi",  "--http-socket", "0.0.0.0:8081", "--module", "app:app", "--processes", "2", "--threads",  "4" ]

