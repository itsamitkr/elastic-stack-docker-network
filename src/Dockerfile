FROM python:3.8-slim

MAINTAINER Amit Kumar <"Singhakumar.18@gmail.com">

WORKDIR /usr/src/app

COPY . ./

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]