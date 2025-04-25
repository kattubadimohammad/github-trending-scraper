FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app

# Explicitly set the working directory before running Uvicorn
WORKDIR /app/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
