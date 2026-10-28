ARG PYTHON_VERSION=3.11-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# psycopg2-binary 등 모든 의존성이 wheel로 제공되므로 gcc/libpq-dev는 필요 없다.

RUN mkdir -p /code

WORKDIR /code

RUN pip install --no-cache-dir --upgrade pip poetry

COPY pyproject.toml poetry.lock /code/

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root --no-interaction \
    && rm -rf /root/.cache

COPY . /code

RUN chmod +x /code/entrypoint.sh

# SECRET_KEY 등 비밀값은 Render 환경변수에서 주입된다.

EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]
