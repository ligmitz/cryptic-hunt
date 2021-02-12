ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

WORKDIR /app

RUN apt-get update && apt-get -y install cron
RUN pip install -U pip wheel setuptools

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

COPY run.sh /app/

COPY backup-db-cron /etc/cron.d/backup-db
RUN chmod 0744 /etc/cron.d/backup-db
RUN crontab /etc/cron.d/backup-db
RUN service cron start

ENTRYPOINT ["bash", "run.sh"]