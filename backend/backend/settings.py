"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from datetime import timedelta

from backend import CONFIG

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ym2u%hpbs7o3nk=-j(8kcr!!-4q$^g54bfu@&whqc%gtta*l26'

GOOGLE_AUTH_SECRET_KEY = 'G-q2QZkS2k60rutAMPpDhhlX'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_rest_passwordreset',
    'corsheaders',
    'drf_yasg',
    'djoser',
    'authentication',
    'root',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000'
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ]
}
AUTH_USER_MODEL = 'authentication.User'

SIMPLE_JWT = {
    # 'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3),
}


DJOSER = {
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'EMAIL': {'confirmation': 'authentication.views.ConfirmationEmail'},
}

DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomNumberTokenGenerator",
    "OPTIONS": {
        "min_number": 10000,
        "max_number": 99999
    }
}
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

}


INDUSTRY_CHOICES = [('Accounting/Taxation', 'Accounting/Taxation'), ('Auditing', 'Auditing'), ('Admin', 'Admin'),
                    ('Agent', 'Agent'),
                    ('Airline Reservation/ticketing/travel', 'Airline Reservation/ticketing/travel'),
                    ('Analytics/Business Intelligence', 'Analytics/Business Intelligence'),
                    ('Anchoring/TV/Films/Production', 'Anchoring/TV/Films/Production'),
                    ('Architecture/Interior Design', 'Architecture/Interior Design'),
                    ('Art Director/Graphic/Web Designer', 'Art Director/Graphic/Web Designer'),
                    ('Backend Operations', 'Backend Operations'), ('Banking/Insurance', 'Banking/Insurance'),
                    ('Beauty/Fitness/Spa services', 'Beauty/Fitness/Spa services'),
                    ('Company secretary (CS)', 'Company secretary (CS)'), ('Computer Operator', 'Computer Operator'),
                    ('Consulting', 'Consulting'),
                    ('Content Writer/Editor/Journalist', 'Content Writer/Editor/Journalist'),
                    ('Corporate Planning/Consulting', 'Corporate Planning/Consulting'),
                    ('CSR/Sustainability', 'CSR/Sustainability'), ('Customer Service', 'Customer Service'),
                    ('Database Administrator (DBA)', 'Database Administrator (DBA)'), ('Data entry', 'Data entry'),
                    ('Digital Marketing/SEM', 'Digital Marketing/SEM'),
                    ('Engineering Design / R & D', 'Engineering Design / R & D'), ('ERP/CRM', 'ERP/CRM'),
                    ('Export/Import Merchandising', 'Export/Import Merchandising'),
                    ('Fashion Designer', 'Fashion Designer'),
                    ('Fashion/Garments merchandising', 'Fashion/Garments merchandising'), ('Finance', 'Finance'),
                    ('Fresher', 'Fresher'), ('Hotel/Restaurant Management', 'Hotel/Restaurant Management'),
                    ('Hotels/Restaurants', 'Hotels/Restaurants'),
                    ('HR - Payroll/Business Partner/General', 'HR - Payroll/Business Partner/General'),
                    ('HR - Recruiter', 'HR - Recruiter'),
                    ('HR/Administration/International Services', 'HR/Administration/International Services'), (
                        'IT Software - Application Programming/Maintenance',
                        'IT Software - Application Programming/Maintenance'),
                    ('IT Software - Client Server', 'IT Software - Client Server'),
                    ('IT Software - DBA/Data warehousing', 'IT Software - DBA/Data warehousing'), (
                        'IT Software - Embedded/EDA/VLSI/ASIC/Chip Design',
                        'IT Software - Embedded/EDA/VLSI/ASIC/Chip Design'),
                    ('IT/Hardware/telecom/Technical Staff/Support', 'IT/Hardware/telecom/Technical Staff/Support'),
                    ('ITES/BPO/KPO/Customer Service/Operations', 'ITES/BPO/KPO/Customer Service/Operations'),
                    ('Language Specialist', 'Language Specialist'), ('Legal', 'Legal'), ('Mainframes', 'Mainframes'),
                    ('Marketing/Advertising/Market Research', 'Marketing/Advertising/Market Research'),
                    ('Media Planning', 'Media Planning'), ('Medical Professional/Healthcare practitioner/Technician',
                                                           'Medical Professional/Healthcare practitioner/Technician'),
                    ('Middleware', 'Middleware'), ('Mobile', 'Mobile'),
                    ('Network administration', 'Network administration'), ('Network security', 'Network security'),
                    ('Other', 'Other'), ('Packaging', 'Packaging'), ('Personal Assistant', 'Personal Assistant'),
                    ('Pharma/Biotech/Healthcare/Medical/R&D', 'Pharma/Biotech/Healthcare/Medical/R&D'),
                    ('PR/Corporate Communication', 'PR/Corporate Communication'),
                    ('Procurement Jobs', 'Procurement Jobs'), ('Product Management', 'Product Management'),
                    ('Production/Maintenance/Quality', 'Production/Maintenance/Quality'),
                    ('Program Management', 'Program Management'), ('Project Management', 'Project Management'),
                    ('Purchase/Logistics/Supply Chain', 'Purchase/Logistics/Supply Chain'),
                    ('QA/Testing', 'QA/Testing'), ('Quality Control Jobs', 'Quality Control Jobs'),
                    ('Research & Development (R&D)', 'Research & Development (R&D)'),
                    ('Sales/BD/Client Servicing', 'Sales/BD/Client Servicing'),
                    ('Secretary/Front Office', 'Secretary/Front Office'),
                    ('Software Development', 'Software Development'),
                    ('Self employed/Consultants', 'Self employed/Consultants'),
                    ('Service Engineering', 'Service Engineering'), ('Shipping', 'Shipping'),
                    ('Site engineering', 'Site engineering'), ('System Programming', 'System Programming'),
                    ('Systems/EDP/MIS', 'Systems/EDP/MIS'), ('Teaching/Education', 'Teaching/Education'),
                    ('Telecalling', 'Telecalling'), ('Telecom Software', 'Telecom Software'),
                    ('Ticketing/Travel/Airlines', 'Ticketing/Travel/Airlines'),
                    ('Web Designer/UI/UX Designer', 'Web Designer/UI/UX Designer')]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': CONFIG.DATABASE['ENGINE'],
        'NAME': CONFIG.DATABASE['NAME'],
        'USER': CONFIG.DATABASE['USER'],
        'PASSWORD': CONFIG.DATABASE['PASSWORD'],
        'HOST': CONFIG.DATABASE['HOST'],
        'PORT': CONFIG.DATABASE['PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = CONFIG.EMAIL_HOST
EMAIL_HOST_USER = CONFIG.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = CONFIG.EMAIL_HOST_PASSWORD
EMAIL_PORT = CONFIG.EMAIL_PORT
EMAIL_USE_TLS = CONFIG.EMAIL_USE_TLS

DEFAULT_FROM_EMAIL = CONFIG.DEFAULT_FROM_EMAIL
HELLO_RECIPIENTS = CONFIG.HELLO_RECIPIENTS

FRONTEND_URL = CONFIG.FRONTEND_URL
PROFILE_PICTURE = 'profile_picture'
RESUME_STORE = 'resumes'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
