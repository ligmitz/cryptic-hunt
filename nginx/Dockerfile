ARG NGINX_VERSION
FROM nginx:${NGINX_VERSION}

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/
