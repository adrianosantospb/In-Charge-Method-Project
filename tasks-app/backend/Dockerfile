# syntax=docker/dockerfile:1

# ---- base: dependencies only -------------------------------------------------
FROM python:3.13-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd --create-home --uid 10001 app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ---- test: adds test tools and the tests ------------------------------------
FROM base AS test
COPY requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements-test.txt
COPY pyproject.toml ./
COPY app app
COPY alembic alembic
COPY alembic.ini ./
COPY tests tests
# The files stay read-only for the app user; it only needs to create the ruff and pytest
# caches in /app.
RUN chown app:app /app
USER app
CMD ["pytest"]

# ---- dev: code is mounted from the host, server reloads on change ------------
FROM test AS dev
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]

# ---- production: only what runs the API --------------------------------------
FROM base AS production
COPY app app
COPY alembic alembic
COPY alembic.ini ./
USER app
EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
