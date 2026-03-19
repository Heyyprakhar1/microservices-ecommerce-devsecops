FROM python:3.13-slim

WORKDIR /app

COPY . .

EXPOSE 5002

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "run.py"]
