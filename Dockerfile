FROM python:3

ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade pip

RUN mkdir /app
WORKDIR /app

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

EXPOSE 8000/tcp
