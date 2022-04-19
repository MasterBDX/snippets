import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-he+!yqy7)1=8*%u0!mb*2d0xo(syyw#01r#-0l=&zcfor28gku'

DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


BASE_URL = 'http://127.0.0.1:8000'

VENV_PATH = BASE_DIR.parent
STATIC_SERVER = VENV_PATH / 'static_server'
# ------------

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = STATIC_SERVER / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = STATIC_SERVER / 'media'
