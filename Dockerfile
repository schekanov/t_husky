FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

ADD . /code/
