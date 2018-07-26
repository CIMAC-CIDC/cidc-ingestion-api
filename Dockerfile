FROM python:3.6

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY . /app
WORKDIR /app
