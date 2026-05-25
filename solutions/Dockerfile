FROM python:3.12-slim

WORKDIR /app
RUN pip install --upgrade pip --root-user-action ignore

COPY pyproject.toml .
COPY README.md .

RUN pip install uv --root-user-action ignore
RUN uv venv
RUN uv sync

COPY books_scraper books_scraper
WORKDIR /app/books_scraper