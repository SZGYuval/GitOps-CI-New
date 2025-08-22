FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY python_app ./python_app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "python_app.wsgi:app", "--workers", "2"]
