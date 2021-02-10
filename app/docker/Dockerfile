ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

WORKDIR /app

RUN pip install -U pip wheel setuptools

COPY requirements.txt /app/ 

RUN pip install -r requirements.txt

COPY ../ .

COPY entrypoint.sh /app/


