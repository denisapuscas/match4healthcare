from match4healthcare.settings.common import *
from os.path import abspath, basename, dirname, join, normpath


# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(ki437obe@zig%4t)fiydfmok1*l6l=d5#uqyz^i-!y@j$n7ku'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(RUN_DIR, 'db.sqlite3'),
    }
}

# =============== MAIL RELAY SERVER CONFIGURATION ===============
# Don't use our domain, prevent bad reputation
NOREPLY_MAIL = 'match4healthcare-DEVELOPMENT<noreply@example.de>'

# Possible values are 'file', 'external', 'sendgrid'
# For storing mails local in files files, sending external (uberspace) or sending over sendgrid (production like)
mail_relay_option = 'sendgrid'

# +++ Store files locally
if mail_relay_option == 'file':
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

# +++ Use local debug server
elif mail_relay_option == 'external':
    EMAIL_HOST = 'spahr.uberspace.de'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'noreply@medisvs.spahr.uberspace.de'
    EMAIL_HOST_PASSWORD = 'jonathan'
    EMAIL_USE_TLS = False

# +++ Use sendgrid
elif mail_relay_option == 'sendgrid':
    # Use API instead of SMTP server
    use_sendgrid_api = True

    # Retrieve sendgrid api key
    SENDGRID_SECRET_FILE = normpath(join(RUN_DIR, 'SENDGRID.key'))
    SENDGRID_API_KEY = open(SENDGRID_SECRET_FILE).read().strip()

    if use_sendgrid_api:
        # Using the API
        EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
        # Disable sendbox mode to send actual emails
        SENDGRID_SANDBOX_MODE_IN_DEBUG = False

        # Disable all tracking options
        SENDGRID_TRACK_EMAIL_OPENS = False
        SENDGRID_TRACK_CLICKS_HTML = False
        SENDGRID_TRACK_CLICKS_PLAIN = False

    else:
        # Normal SMTP
        EMAIL_HOST = 'smtp.sendgrid.net'
        EMAIL_HOST_USER = 'apikey'
        EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
        EMAIL_PORT = 587
        EMAIL_USE_TLS = True

else:
    # ToDo add logger message instead?
    print("No email option selected")
    exit(1)
