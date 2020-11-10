FROM python:3

ARG HTTP_PROXY
ARG HTTPS_PROXY

RUN { \
    echo 'Acquire::http::proxy "'${HTTP_PROXY}'";'; \
    echo 'Acquire::https::proxy "'${HTTPS_PROXY}'";'; \
} | tee /etc/apt/apt.conf

RUN apt update && apt install -y \
	pulseaudio \
        sox \
	libsox-fmt-all \
	open-jtalk \
	open-jtalk-mecab-naist-jdic

RUN pip3 install -U pip
ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

ADD ./app/ /code

CMD [ "python3", "/code/main.py" ]

