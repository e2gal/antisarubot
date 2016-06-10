FROM ubuntu:14.04

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

WORKDIR /usr/local/i2vbot

RUN git clone https://github.com/e2gal/i2vbot . && git submodule update --init
RUN virtualenv --system-site-packages venv
RUN . venv/bin/activate && for r in `cat requirements.txt`; do pip install $r; done

# Change this with your telegram bot token.
RUN echo 'TOKEN = "[YOUR_TELEGRAM_BOT_TOKEN]"' > bottoken.py

RUN sh get_models.sh

CMD . venv/bin/activate && python2 main.py
