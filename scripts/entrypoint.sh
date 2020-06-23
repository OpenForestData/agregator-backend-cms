#!/bin/bash
/app/scripts/wait_for.sh ofd_agregator_psql:5432 -t 15 -- echo "Database (PSQL) is up!"

python /app/manage.py buildapp --profile settings

python /app/manage.py runserver 0.0.0.0:8000
