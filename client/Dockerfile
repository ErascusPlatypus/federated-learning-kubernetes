FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install flwr river numpy

CMD ["python", "client.py"]
