# backend/Dockerfile

FROM python:3.8-slim

WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]