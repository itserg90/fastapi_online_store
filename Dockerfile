FROM python:3.11

RUN pip install --upgrade pip && pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction

COPY . .
