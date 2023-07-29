FROM python:3.11-slim

WORKDIR /app

EXPOSE 7860

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .
