
SENDGRID_API_KEY = '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'

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


AWS_ACCESS_KEY_ID = 'AKIAT7YG4LQXU7BTMN5L'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'staging-media.interviewleap.com'
AWS_DEFAULT_ACL = None
