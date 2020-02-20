FROM nginx:1.15-alpine

RUN apk update
RUN apk add openssl

RUN rm -f /etc/nginx/conf.d/*
RUN mkdir /certs
RUN mkdir /www
RUN mkdir /etc/nginx/snippets

COPY index.html /www
COPY default.conf /etc/nginx/conf.d
COPY self-signed.conf /etc/nginx/snippets
COPY ssl-params.conf /etc/nginx/snippets


COPY nginx-selfsigned.crt /certs
COPY nginx-selfsigned.key /certs

COPY dhparam.pem /certs

COPY request.crt /certs
COPY server.key /certs