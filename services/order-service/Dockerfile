# Stage 1: Builder
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final — non-root user
FROM python:3.12-slim
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /install /usr/local
COPY app/ ./app/
COPY run.py .
RUN chown -R appuser:appgroup /app
USER appuser
EXPOSE 5003
CMD ["python3", "run.py"]
