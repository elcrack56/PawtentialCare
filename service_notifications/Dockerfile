FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
ENV PYTHONPATH=/app
CMD ["python", "app/consumer.py"]
