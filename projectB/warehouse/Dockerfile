FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies including netcat
RUN apt-get update && apt install -y --no-install-recommends \
    vim \
    libpq-dev \
    python3-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall redis -y && \
    pip install --no-cache-dir 'redis>=7.4.0' --force-reinstall

RUN echo "=== VERIFY REDIS ===" && \
    python -c "import redis; print(f'Redis version: {redis.__version__}'); print(f'Redis location: {redis.__file__}')" && \
    python -c "from redis.client import Redis; print('Import successful')"

COPY . .

RUN chmod +x ./entrypoint.sh

EXPOSE 8001

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
