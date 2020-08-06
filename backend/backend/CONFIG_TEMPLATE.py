
SENDGRID_API_KEY = ''

DATABASE = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': ''
}

DEBUG = False
ALLOWED_HOSTS = []

FRONTEND_URL = "http://localhost:3000"

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'Anil from Equiv.in<anil@equiv.in>'
HELLO_RECIPIENTS = 'anil@equiv.in'


AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''
AWS_DEFAULT_ACL = None

PAYMENT_API_KEY = ''
PAYMENT_AUTH_TOKEN = ''
PAYMENT_SALT = ''