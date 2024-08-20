
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-u1dme*97rgy9$@&_-!j4l-2ncun_m*7vb(j6!dluw@!zy47w+j'

DEBUG = True

ALLOWED_HOSTS = ['192.168.18.6', 'localhost', '192.168.18.43']



CORS_ORIGIN_ALLOW_ALL = True


CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]



INSTALLED_APPS = [
    'django.contrib.admin',
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_auths',
    'menu',
    'course',
    'category',

    'rest_framework',
    'drf_spectacular',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'brewing_pathshala.urls'

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

WSGI_APPLICATION = 'brewing_pathshala.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'brewing_pathshala',
        'USER': 'postgres',
        'PASSWORD': 'CLB26C70BB',
        'HOST': 'localhost',
        'PORT': '5432',
        'TIME_ZONE': 'UTC',  # Ensure this is included
        
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'user_auths.User'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/anishchengre/django/brewing-pathshala/debug.log',
        },
    },
   
}





REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'usable.custom_authentication.CustomAuthentication'
     ],
    'DEFAULT_PERMISSION_CLASSES': [
        'usable.permission.DynamicPermission',
    ],
    'EXCEPTION_HANDLER': 'usable.custom_exceptions.custom_exception_handler',

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}



SPECTACULAR_SETTINGS = {
    'TITLE': 'Brewing Pathshala',
    'DESCRIPTION': 'Brewing Pathshala is an academy for coffee and barista',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],  # Allow access to the schema
    # OTHER SETTINGS
}

