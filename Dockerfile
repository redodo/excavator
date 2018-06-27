FROM python:3

ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade pip

RUN mkdir /api
WORKDIR /api

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

CMD ["python", "serve.py"]

EXPOSE 8000/tcp
