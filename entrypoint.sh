#!/bin/sh

python manager.py migrate --no-input

python manager.py collecstatic --no-input

gunicorn crm.wsgi:application --bind 0.0.0:8000