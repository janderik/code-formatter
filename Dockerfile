FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    black \
    isort \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e .

ENTRYPOINT ["python", "cli.py"]
