#!/bin/bash
/app/scripts/wait_for.sh ofdAgregatorCMSPsql:5432 -t 15 -- echo "Database (ofdAgregatorCMSPsql) is up!"

python /app/manage.py makemigrations
python /app/manage.py migrate
python /app/manage.py collectstatic --noinput

python /app/manage.py runserver 0.0.0.0:8000
