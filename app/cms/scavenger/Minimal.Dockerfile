FROM python:3

COPY requirements-dev.in requirements-dev.in

COPY requirements.in requirements.in

RUN pip install --upgrade pip pip-tools

RUN pip-compile requirements.in requirements-dev.in --output-file requirements.txt
RUN pip install -r requirements.txt

COPY . /app/scavenger

WORKDIR /app/scavenger
