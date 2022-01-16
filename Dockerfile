FROM alpine

RUN apk add --no-cache \
    bash

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY entrypoint.py /usr/local/bin/entrypoint.py
COPY requirements.txt /usr/local/bin/requirements.txt
COPY sample_push_event.json /sample_push_event.json

RUN pip install -r /usr/local/bin/requirements.txt

ENTRYPOINT ["python3", "/usr/local/bin/entrypoint.py"]
# CMD ["/bin/bash"]
