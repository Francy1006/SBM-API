#!/bin/sh 

echo "Starting Django application"

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run Django system migrations
echo "Running Django system migrations..."
python manage.py migrate --run-syncdb

# Create superuser if it doesn't exist using environment variables
echo "Checking if superuser exists..."
python manage.py shell -c "
from django.contrib.auth.models import User
import os

username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'sbm-admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'operacione@ditalypasta.cl')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'sbm123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created successfully')
else:
    print(f'Superuser {username} already exists')
"

# Alternative method using createsuperuser command (uncomment if needed)
# echo "Creating superuser with createsuperuser command..."
# python manage.py createsuperuser --username sbm-admin --email operacione@ditalypasta.cl --noinput

echo "Django application is ready!"
exec "$@"
