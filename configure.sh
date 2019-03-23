#!/usr/bin/env bash

# Run on docker container - sets the default superuser for the DB

DEFAULT_SU_NAME="admin"
DEFAULT_SU_PWD="adminpass"
DEFAULT_SU_EMAIL="admin@example.com"

# Set the default superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$DEFAULT_SU_NAME', '$DEFAULT_SU_EMAIL', '$DEFAULT_SU_PWD')" | pipenv run ./manage.py shell