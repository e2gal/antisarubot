FROM ubuntu:14.04

ARG token

# Biar ngebut kalau di Indonesia.
RUN sed -i 's/archive\.ubuntu\.com/kambing.ui.ac.id/' /etc/apt/sources.list

RUN apt-get -y update && apt-get -y --no-install-recommends install \
    build-essential git ca-certificates wget \
    libopenblas-dev \
    python-pillow \
    python-matplotlib \
    python-scipy \
    python-dev \
    python-virtualenv

WORKDIR /usr/local/i2vbot-docker

RUN mkdir i2vbot
VOLUME i2vbot

# A hack to load the requirements file
RUN curl https://raw.githubusercontent.com/e2gal/i2vbot/master/requirements.txt \
    -o requirements.txt
RUN virtualenv --system-site-packages venv
RUN . venv/bin/activate && for r in `cat requirements.txt`; do pip install $r; done
RUN rm requirements.txt

CMD . venv/bin/activate && python2 i2vbot/main.py
