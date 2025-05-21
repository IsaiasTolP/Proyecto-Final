#!/bin/bash
echo "▶️ Applying migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "🚀 Starting RQ worker..."
python manage.py rqworker &

echo "🟢 Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
