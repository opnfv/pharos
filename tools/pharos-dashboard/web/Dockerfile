FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD ./requirements.txt /config/
RUN pip install -r /config/requirements.txt
RUN mkdir -p /pharos_dashboard/src
WORKDIR /pharos_dashboard/src
