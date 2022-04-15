FROM python:3 as builder

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

ARG requirements="requirements.in"

COPY requirements-*.in ./

COPY requirements.in requirements.in

RUN pip install --upgrade pip pip-tools

RUN pip-compile ${requirements} --output-file requirements.txt
RUN pip install --prefer-binary -r requirements.txt

FROM python:3

COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

COPY . /app/scavenger

WORKDIR /app/scavenger
