#!/bin/bash
echo "▶️ Applying migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic

mkdir media
cd media/
mkdir docs profile_pics project_images
cd docs/
gdown https://drive.google.com/uc?id=1RxcVvWn1c_l-qbYccJfMh-f_BIV4abZ_
cd ../project_images/
gdown https://drive.google.com/uc?id=16YPQ7nNOUU9OU5PHEzpGHdTZc5zpO5qd
cd ../profile_pics/
gdown https://drive.google.com/uc?id=12syL4-FwDLMrg9yfgUyQkaeAmu0OpOMF
cd ../../

echo "🚀 Starting RQ worker..."
python manage.py rqworker &

echo "🟢 Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
