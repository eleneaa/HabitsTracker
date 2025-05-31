FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc libpq-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=habit_tracker.settings
ENV PYTHONPATH=/app

CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn habit_tracker.wsgi:application --bind 0.0.0.0:8000"]
