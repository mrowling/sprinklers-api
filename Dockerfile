FROM arm32v7/python:3.8.3-alpine3.12

WORKDIR /usr/src/app

ARG TZ='Australia/Sydney'

ENV DEFAULT_TZ ${TZ}

COPY requirements.txt ./

RUN apk upgrade --update \
  && apk add -U tzdata \
  && apk add build-base \
  && cp /usr/share/zoneinfo/${DEFAULT_TZ} /etc/localtime \
  && apk del tzdata \
  && pip install --no-cache-dir -r requirements.txt \
  && pip install gunicorn \
  && apk del build-base \
  && rm -rf \
  /var/cache/apk/*

COPY . .

CMD [ "gunicorn", "-b", "0.0.0.0:8000", "app.app" ]