FROM python:3.8.3-alpine3.12

WORKDIR /usr/src/app

ARG TZ='Australia/Sydney'

ENV DEFAULT_TZ ${TZ}

RUN apk upgrade --update \
  && apk add -U tzdata \
  && cp /usr/share/zoneinfo/${DEFAULT_TZ} /etc/localtime \
  && apk del tzdata \
  && rm -rf \
  /var/cache/apk/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || pip install rpi-gpio-emu
RUN pip install gunicorn

COPY . .

CMD [ "gunicorn", "-b 0.0.0.0:8000", "--reload", "app.app" ]