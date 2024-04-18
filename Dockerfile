FROM python:3.12

WORKDIR /petalsync

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -


ENV PATH="/etc/poetry/bin:${PATH}"

SHELL ["/bin/bash", "-c"]

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY petalsync .

RUN python -m venv /opt/venv

RUN /opt/venv/bin/python -m pip install --upgrade pip
RUN apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN apt-get update && apt-get install -y libsmbclient-dev
RUN apt-get update && apt-get install -y libgirepository1.0-dev

RUN /opt/venv/bin/python -m pip install uvicorn

EXPOSE 8000 5000

CMD supervisord -c /etc/supervisor/conf.d/supervisord.conf
