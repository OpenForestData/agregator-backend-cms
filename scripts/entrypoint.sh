#!/bin/bash
/app/scripts/wait_for.sh ofd_agregator_cms_psql:5432 -t 15 -- echo "Database (ofd_agregator_cms_psql) is up!"

python /app/manage.py buildapp --profile development

python /app/manage.py runserver 0.0.0.0:8000
