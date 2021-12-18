FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn

COPY . .

ENV FLASK_APP=app



CMD ["python", "app.py"]
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8081", "app:app", "--log-file", "gunicorn.log", "--log-level",  "DEBUG"]

