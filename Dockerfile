ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

WORKDIR /app

COPY requirements.txt /app/ 

RUN pip install -r requirements.txt

COPY . /app/

COPY entrypoint.sh /app/

ENTRYPOINT [ "sh", "entrypoint.sh" ]

