ARG NGINX_VERSION
FROM nginx:${NGINX_VERSION}

WORKDIR /main

RUN apt-get update && apt-get install --yes certbot python-certbot-nginx vim netcat less python3 apache2-utils

COPY run nginx.conf ./

CMD ["bash", "run"]
