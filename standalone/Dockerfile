# --- Stage 1: Build frontend assets ---
FROM node:20 AS frontend-builder

# Copy source and build static assets
WORKDIR /app

COPY . .

# Enable Corepack to use the defined packageManager in package.json
RUN corepack enable
# Install dependencies
RUN yarn install
RUN yarn build:static

# --- Stage 2: Main Django image ---
FROM python:3.11-slim-bookworm AS app
LABEL src=https://github.com/django-helpdesk/django-helpdesk
# Keep update + install in a single layer so the package index is never cached
# separately from the install (stale indexes cause 404s on moved .deb files).
RUN apt-get update && apt-get install -yqq \
   postgresql-common \
   postgresql-client \
   cron \
   git \
   && rm -rf /var/lib/apt/lists/*

# Copy directories
COPY src/ /opt/django-helpdesk/src/
COPY standalone/ /opt/django-helpdesk/standalone/
COPY --from=frontend-builder /app/src/helpdesk/static/helpdesk/vendor /opt/django-helpdesk/src/helpdesk/static/helpdesk/vendor

# Copy files
COPY pyproject.toml /opt/django-helpdesk/
COPY README.rst /opt/django-helpdesk/

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN pip3 install --upgrade pip
RUN pip3 install packaging
WORKDIR /opt/django-helpdesk

ENV UV_SYSTEM_PYTHON=1
RUN uv sync
RUN uv pip install -r /opt/django-helpdesk/standalone/requirements.txt

WORKDIR /opt/django-helpdesk/standalone
ENV DJANGO_SETTINGS_MODULE=standalone.config.settings
ENV PYTHONPATH=/opt/django-helpdesk/src:/opt/django-helpdesk

RUN DJANGO_HELPDESK_SECRET_KEY=foo python3 manage.py collectstatic --noinput

RUN echo "* * * * * root . /etc/env && /usr/local/bin/python3 /opt/django-helpdesk/standalone/manage.py get_email >> /var/log/cron.log 2>&1" > /etc/crontab
RUN chmod 0644 /etc/crontab
# Make sure entrypoint script is executable
RUN chmod +x /opt/django-helpdesk/standalone/entrypoint.sh
ENTRYPOINT [ "/opt/django-helpdesk/standalone/entrypoint.sh" ]
