FROM python:3.11-slim

WORKDIR /application

COPY ./requirements.txt /application/requirements.txt

RUN apt-get update && apt-get install -y build-essential gcc libffi-dev libpq-dev curl && rm -rf /var/lib/apt/lists/*

RUN pip install --verbose --no-cache-dir -r /application/requirements.txt

COPY . /application/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]