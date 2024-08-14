# Use an official Python runtime as a parent image
FROM python:3.9

ENV HTTP_PROXY=http://10.187.215.117:3128
ENV HTTPS_PROXY=http://10.187.215.117:3128

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app/

RUN mkdir -p /etc/pip.conf.d \
    && echo "[global]" > /etc/pip.conf \
    && echo "index-url = https://pypi.org/simple/" >> /etc/pip.conf \
    && echo "[index]" >> /etc/pip.conf \
    && echo "index = https://pypi.org/simple/" >> /etc/pip.conf \
    && echo "proxy = http://10.187.215.117:3128" >> /etc/pip.conf
#
RUN pip config list
RUN mkdir -p /etc/docker/daemon.json.d
#
RUN echo '{"http-proxy": "http://10.187.215.117:3128","https-proxy": "http://10.187.215.117:3128","dns": ["10.54.12.44", "10.187.50.203"]}' > /etc/docker/daemon.json


RUN cat /etc/docker/daemon.json
RUN cat /etc/resolv.conf

RUN echo $(cat /etc/resolv.conf)

RUN pip install virtualenv --proxy http://10.187.215.117:3128 -v

RUN python3 -m virtualenv venv

RUN . /app/venv/bin/activate

RUN pip install django --proxy http://10.187.215.117:3128 -v

RUN pip install mysqlclient

EXPOSE 8222

CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8222"]