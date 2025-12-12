#!/usr/bin/env bash
set -o errexit  

cd project 

pip install -r ../requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate

if [[$CREATE_SUPERUSER]];
then
    python manage.py createsuperuser --noinput
fi