"""
Django settings for django-helpdesk demodesk project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# Read SECRET_KEY from DJANGO_HELPDESK_SECRET_KEY env var
try:
    SECRET_KEY = os.environ["DJANGO_HELPDESK_SECRET_KEY"]
except KeyError:
    raise Exception("DJANGO_HELPDESK_SECRET_KEY environment variable is not set")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_HELPDESK_ALLOWED_HOSTS", "*, localhost, 0.0.0.0"
).split(",")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    # "unfold.contrib.import_export",  # optional, if django-import-export package is used
    # "unfold.contrib.guardian",  # optional, if django-guardian package is used
    # "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    # "unfold.contrib.location_field",  # optional, if django-location-field package is used
    # "unfold.contrib.constance",  # optional, if django-constance package is used
    # "unfold.contrib.hijack",  # optional, if django-hijack package is used
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    "bootstrap4form",
    "helpdesk",  # This is us!
    "rest_framework",  # required for the API
    # Must be last: re-themes other apps' admin registrations with Unfold.
    "standalone.unfold_admin",
]

# Default teams mode to disabled unless overridden by an environment variable set to "false"
HELPDESK_TEAMS_MODE_ENABLED = (
    os.getenv("HELPDESK_TEAMS_MODE_ENABLED", "false").lower() == "true"
)
if HELPDESK_TEAMS_MODE_ENABLED:
    INSTALLED_APPS.extend(
        [
            "account",  # Required by pinax-teams
            "pinax.invitations",  # required by pinax-teams
            "pinax.teams",  # team support
            "reversion",  # required by pinax-teams
        ]
    )

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "standalone.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": True,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "standalone.config.wsgi.application"


# django-helpdesk configuration settings
# You can override django-helpdesk's defaults by redefining them here.
# To see what settings are available, see the docs/configuration.rst
# file for more information.
# Some common settings are below.

HELPDESK_DEFAULT_SETTINGS = {
    "use_email_as_submitter": os.environ.get("HELPDESK_USE_EMAIL_AS_SUBMITTER", "True")
    == "True",
    "email_on_ticket_assign": os.environ.get("HELPDESK_EMAIL_ON_TICKET_ASSIGN", "True")
    == "True",
    "email_on_ticket_change": os.environ.get("HELPDESK_EMAIL_ON_TICKET_CHANGE", "True")
    == "True",
    "login_view_ticketlist": os.environ.get("HELPDESK_LOGIN_VIEW_TICKETLIST", "True")
    == "True",
    "preset_replies": os.environ.get("HELPDESK_PRESET_REPLIES", "True") == "True",
    "tickets_per_page": os.environ.get("HELPDESK_TICKETS_PER_PAGE", "25"),
}

# Should the public web portal be enabled?
HELPDESK_PUBLIC_ENABLED = os.environ.get("HELPDESK_PUBLIC_ENABLED", "True") == "True"
HELPDESK_VIEW_A_TICKET_PUBLIC = (
    os.environ.get("HELPDESK_VIEW_A_TICKET_PUBLIC", "True") == "True"
)
HELPDESK_SUBMIT_A_TICKET_PUBLIC = (
    os.environ.get("HELPDESK_SUBMIT_A_TICKET_PUBLIC", "True") == "True"
)

# Restrict who can submit via the public form to approved email domains.
# Comma-separated env var (e.g. "addleman.tech,example.com"); empty = no
# restriction. Enforced by a custom public form plugged in through helpdesk's
# own HELPDESK_PUBLIC_TICKET_FORM_CLASS hook (no upstream edits).
HELPDESK_ALLOWED_SUBMITTER_DOMAINS = [
    d.strip()
    for d in os.environ.get("HELPDESK_ALLOWED_SUBMITTER_DOMAINS", "").split(",")
    if d.strip()
]
HELPDESK_PUBLIC_TICKET_FORM_CLASS = (
    "standalone.config.forms.DomainRestrictedPublicTicketForm"
)

# Should the Knowledgebase be enabled?
HELPDESK_KB_ENABLED = os.environ.get("HELPDESK_KB_ENABLED", "True") == "True"

HELPDESK_TICKETS_TIMELINE_ENABLED = (
    os.environ.get("HELPDESK_TICKETS_TIMELINE_ENABLED", "True") == "True"
)

# Instead of showing the public web portal first,
# we can instead redirect users straight to the login page.
HELPDESK_REDIRECT_TO_LOGIN_BY_DEFAULT = (
    os.environ.get("HELPDESK_REDIRECT_TO_LOGIN_BY_DEFAULT", "False") == "True"
)
LOGIN_URL = "helpdesk:login"
LOGIN_REDIRECT_URL = "helpdesk:home"


# --- Custom ticket statuses ---------------------------------------------
# django-helpdesk reads ticket statuses from these settings (see
# helpdesk/settings.py). `status` is an IntegerField, so adding/removing
# choices needs no database migration.
#
# We keep six statuses. "Resolved" (built-in id 3) is intentionally dropped
# so only "Closed" remains; its constant stays defined internally, so the
# code paths that reference it simply never fire. "Reopened" is mapped onto
# "Open" (same id) so a ticket reopened by an email reply (helpdesk/email.py
# auto-sets REOPENED_STATUS) returns to the Open column instead of needing a
# column of its own.
HELPDESK_TICKET_REOPENED_STATUS = 1  # treat "reopened" as "open"

# The order of entries here is the left-to-right order of the Kanban columns.
HELPDESK_TICKET_STATUS_CHOICES = (
    (1, "Open"),
    (7, "Needs Review"),
    (6, "In Progress"),
    (8, "On Hold"),
    (4, "Closed"),
    (5, "Duplicate"),
)

# Statuses treated as "active/open": counted in open-ticket lists and
# dashboards, and they block tickets that depend on them.
HELPDESK_TICKET_OPEN_STATUSES = (1, 6, 7, 8)

# Allowed transitions: for a ticket's current status, which statuses the
# update form offers (the Kanban allows dropping into any column).
HELPDESK_TICKET_STATUS_CHOICES_FLOW = {
    1: (1, 7, 6, 8, 4, 5),  # Open
    7: (7, 6, 8, 4, 5),     # Needs Review
    6: (6, 8, 7, 4, 5),     # In Progress
    8: (8, 6, 7, 4, 5),     # On Hold
    4: (4, 1),              # Closed -> reopen to Open
    5: (5, 1),              # Duplicate -> reopen to Open
}


if os.environ.get("DATABASE_URL"):
    # Heroku (and other 12-factor platforms) provide a single DATABASE_URL.
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=os.environ.get("DATABASE_SSL_REQUIRE", "True") == "True",
        )
    }
else:
    DATABASES = {
        # Setup postgress db with postgres as host and db name and read password from env var
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "postgres"),
            "USER": os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.environ.get("POSTGRES_HOST", "postgres"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }


# Sites
# - this allows hosting of more than one site from a single server,
#   in practice you can probably just leave this default if you only
#   host a single site, but read more in the docs:
# https://docs.djangoproject.com/en/1.11/ref/contrib/sites/

SITE_ID = 1


# Sessions
# https://docs.djangoproject.com/en/1.11/topics/http/sessions

SESSION_COOKIE_AGE = 86400  # = 1 day

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Email
# https://docs.djangoproject.com/en/1.11/topics/email/

# This demo uses the console backend, which simply prints emails to the console
# rather than actually sending them out.
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@localhost.localdomain")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "noreply@localhost.localdomain")

if not os.environ.get("EMAIL_HOST") and os.environ.get("MAILGUN_SMTP_SERVER"):
    # Heroku Mailgun add-on provides MAILGUN_SMTP_* instead of EMAIL_*; map them.
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ["MAILGUN_SMTP_SERVER"]
    EMAIL_PORT = int(os.environ.get("MAILGUN_SMTP_PORT", "587"))
    EMAIL_HOST_USER = os.environ["MAILGUN_SMTP_LOGIN"]
    EMAIL_HOST_PASSWORD = os.environ["MAILGUN_SMTP_PASSWORD"]
    EMAIL_USE_TLS = True
elif os.environ.get("EMAIL_HOST", None):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    try:
        EMAIL_HOST = os.environ["EMAIL_HOST"]
    except KeyError:
        raise ImproperlyConfigured("Please set the EMAIL_HOST environment variable.")
    try:
        EMAIL_PORT = os.environ["EMAIL_PORT"]
    except KeyError:
        raise ImproperlyConfigured("Please set the EMAIL_PORT environment variable.")

    try:
        EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"].lower() == "true"
    except KeyError:
        raise ImproperlyConfigured("Please set the EMAIL_USE_TLS environment variable.")

    try:
        EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
    except KeyError:
        raise ImproperlyConfigured("Please set the EMAIL_HOST_USER environment variable.")

    try:
        EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
    except KeyError:
        raise ImproperlyConfigured("Please set the EMAIL_HOST_PASSWORD environment variable.")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# By default, django-helpdesk uses en, but other languages are also available.
# The most complete translations are: es-MX, ru, zh-Hans
# Contribute to our translations via Transifex if you can!
# See CONTRIBUTING.rst for more info.
LANGUAGE_CODE = "en-US"

TIME_ZONE = "UTC"

USE_I18N = True


USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
def normpath(*args):
    return os.path.normpath(os.path.abspath(os.path.join(*args)))


PROJECT_ROOT = normpath(__file__, "..", "..")
STATIC_ROOT = os.environ.get(
    "DJANGO_HELPDESK_STATIC_ROOT", normpath(PROJECT_ROOT, "static")
)
STATIC_URL = os.environ.get("DJANGO_HELPDESK_STATIC_URL", "/static/")

# Project-level static overrides. Files here are collected BEFORE the helpdesk
# app's own static (FileSystemFinder runs before AppDirectoriesFinder), so a
# file at assets/helpdesk/<name> overrides helpdesk's bundled copy. This is how
# we theme the UI without editing the upstream package (e.g. helpdesk-extend.css
# is the override hook loaded last in helpdesk/base-head.html).
STATICFILES_DIRS = [normpath(PROJECT_ROOT, "assets")]

# Let WhiteNoise compress and serve collected static files (no hashed manifest,
# so a missing vendored asset won't fail `collectstatic` during the build).
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Persistent media storage via Cloudinary (keeps ticket attachments off the
# ephemeral dyno filesystem). Activated only when CLOUDINARY_URL is present —
# the Heroku Cloudinary add-on sets it as cloudinary://<key>:<secret>@<cloud>,
# which the cloudinary SDK reads automatically. Without it (e.g. local Docker)
# the default FileSystemStorage above is used. RawMediaCloudinaryStorage stores
# files as-is for any type, which suits arbitrary ticket attachments.
if os.environ.get("CLOUDINARY_URL"):
    INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]
    STORAGES["default"]["BACKEND"] = (
        "cloudinary_storage.storage.RawMediaCloudinaryStorage"
    )


# MEDIA_ROOT is where media uploads are stored.
# We set this to a directory to host file attachments created
# with tickets.
MEDIA_URL = "/media/"
# Overridable so it can point at a writable path (Heroku's filesystem is
# ephemeral, so this is scratch space only — use S3 for durable attachments).
MEDIA_ROOT = os.environ.get("DJANGO_HELPDESK_MEDIA_ROOT", "/data/media")

# for Django 3.2+, set default for autofields:
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",  # Change to 'DEBUG' if you want to print all debug messages as well
            "propagate": True,
        },
    },
}
