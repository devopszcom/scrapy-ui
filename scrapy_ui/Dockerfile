# Author: Cuong Nguyen
#
# Build: docker build -t devopszcom/scrapy_ui:0.1.0 .
#

FROM python:3.6.7-alpine
LABEL maintainer="cuongnb14@gmail.com"

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r /usr/src/app/requirements.txt

COPY . /usr/src/app

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]