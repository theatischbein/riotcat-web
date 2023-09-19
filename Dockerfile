FROM python:3-alpine

RUN apk add gcc musl-dev python3-dev openldap-dev py3-pip
COPY . /opt/riotcat-web/
RUN pip3 install -r /opt/riotcat-web/requirements
WORKDIR /opt/riotcat-web
CMD ["gunicorn", "riotcat.wsgi", "-b", "0.0.0.0:8000"]
