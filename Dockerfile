FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY main.py .
COPY schema.py .
COPY artifacts/ artifacts/

# Expose FastAPI port
EXPOSE 8005

# 🔴 MANDATORY CMD (DO NOT CHANGE)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
