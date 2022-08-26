FROM python:3 as builder

#RUN python -m venv /venv
#ENV PATH="/venv/bin:$PATH"

ARG requirements="requirements.in"

COPY requirements-*.in ./

COPY requirements.in requirements.in

RUN pip install --upgrade pip-tools

RUN pip-compile ${requirements} --output-file requirements.txt

FROM python:3-alpine as slim

RUN apk update && apk add postgresql-dev build-base

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY --from=builder ./requirements.txt ./requirements.txt

RUN pip install --prefer-binary -r requirements.txt

FROM python:3-alpine

COPY --from=slim /venv /venv
ENV PATH="/venv/bin:$PATH"
