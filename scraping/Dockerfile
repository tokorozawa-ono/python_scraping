FROM python:3
RUN set -x && \
  apt-get update && \
  apt-get install -y vim && \
  apt-get install -y cron && \
  mkdir /app
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
WORKDIR /app
ADD requirement.txt /app/
RUN pip install -r requirement.txt
ADD crontmp /app/
RUN crontab crontmp
RUN  /etc/init.d/cron start