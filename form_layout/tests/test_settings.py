# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'og82cu-*+pr6oouypt-u(tj37fi*2qrvi@9oqjk%p*f10#_u_l'

INSTALLED_APPS = (
    'tests',
)

ROOT_URLCONF = 'tests.urls'

DEBUG_PROPAGATE_EXCEPTIONS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}
