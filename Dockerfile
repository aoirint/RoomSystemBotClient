FROM python:3

ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

ADD ./app/ /code

CMD [ "python3", "/code/main.py" ]

