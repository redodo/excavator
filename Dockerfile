FROM python:3

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir /api
WORKDIR /api

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

ENTRYPOINT ["dirtcastle"]
CMD ["runserver"]

EXPOSE 5000/tcp
