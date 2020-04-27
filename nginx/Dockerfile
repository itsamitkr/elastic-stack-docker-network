FROM ubuntu:18.04

MAINTAINER Amit Kumar <"Singhakumar.18@gmail.com">

RUN apt-get update \
    && apt-get install -y nginx \
    && apt-get clean

COPY ./nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080 8081 8082

CMD [ "nginx", "-g", "daemon off;" ]