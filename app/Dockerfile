FROM python:3.10-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update \
    && apk add zlib-dev jpeg-dev gcc musl-dev
RUN apk update \
    && apk add postgresql-dev python3-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install --no-cache -r requirements.txt
COPY . .
