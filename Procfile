release: python standalone/manage.py migrate --noinput
web: gunicorn standalone.config.wsgi:application --log-file - --access-logfile - --workers ${WEB_CONCURRENCY:-3} --timeout ${GUNICORN_TIMEOUT:-60}
