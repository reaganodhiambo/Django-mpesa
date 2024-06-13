#! /bin/sh
source .env


python manage.py migrate 
python manage.py makemigrations

#create superuser
# python manage.py createsuperuser --username admin --email admin@gmail.com --password "$DJANGO_SUPERUSER_PASSWORD"

#start application
python manage.py runserver 0.0.0.0:8000