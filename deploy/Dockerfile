FROM python:3.12-slim-bookworm AS builder
WORKDIR /app
RUN echo 'Acquire::http::Pipeline-Depth "0";' > /etc/apt/apt.conf.d/99custom && \
    echo 'Acquire::http::No-Cache "true";' >> /etc/apt/apt.conf.d/99custom && \
    echo 'Acquire::BrokenProxy "true";' >> /etc/apt/apt.conf.d/99custom
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential libffi-dev \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim-bookworm
WORKDIR /app
RUN echo 'Acquire::http::Pipeline-Depth "0";' > /etc/apt/apt.conf.d/99custom && \
    echo 'Acquire::http::No-Cache "true";' >> /etc/apt/apt.conf.d/99custom && \
    echo 'Acquire::BrokenProxy "true";' >> /etc/apt/apt.conf.d/99custom
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
RUN playwright install chromium
RUN playwright install-deps
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["sh", "-c", "python scripts/migrate.py && uvicorn api.app:app --host 0.0.0.0 --port 8000"]

