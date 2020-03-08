FROM ubuntu:16.04
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
RUN pip3 install pipenv
RUN set -ex && mkdir /app
WORKDIR /app
COPY . /app
RUN pipenv install --dev \
 && pipenv lock -r > requirements.txt
EXPOSE 5000
CMD ["bash", "run.sh"]