# Author: Cuong Nguyen
#
# Build: docker build -t scrapy_ui:0.1.0 .
#

FROM ubuntu:16.04
LABEL maintainer="cuongnb14@gmail.com"

RUN apt-get update -qq

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip build-essential python3-dev \
    libmysqlclient-dev libxml2-dev libxslt1-dev libssl-dev libffi-dev

RUN apt-get install locales && locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r /usr/src/app/requirements.txt

COPY . /usr/src/app

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]