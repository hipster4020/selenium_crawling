FROM ubuntu:20.04

# file copy
COPY requirements.txt requirements.txt

RUN mkdir /scrap/portal
RUN mkdir log

COPY naver_scraper.py /scrap/portal/naver_scraper.py

# 키지 설치시에도 상호작용 방지기능이 적용
ENV DEBIAN_FRONTEND noninteractive

# 설치 실행
RUN apt-get update && apt-get install -y gcc wget gnupg cron vim procps python3.8 python3-pip tzdata rsyslog supervisor
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt-get update && apt-get install -y google-chrome-stable
RUN pip3 install -r requirements.txt

# supervisor file
COPY scrap.conf /etc/supervisor/conf.d/scrap.conf
COPY supervisord.conf /etc/supervisor/supervisord.conf

# crontab file
COPY cron.txt /etc/cron.d/news.cron
RUN chmod 777 /etc/cron.d/news.cron
RUN crontab /etc/cron.d/news.cron
RUN service cron start

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# docker build 시 supervisor 실행
CMD ["/usr/bin/supervisord"]