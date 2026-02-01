FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY schema.py .
COPY artifacts/ artifacts/

# Correct CMD with port 8005
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
