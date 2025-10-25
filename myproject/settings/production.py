# settings/production.py
from .base import *

DEBUG = False  

SECRET_KEY = "django-insecure-7n801@zb(oka0^12ham7cl%v_1#7hyp6%kkfek$-alq$@8r&ig"

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'crimea-yurist.ru',
    'www.crimea-yurist.ru',
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Безопасность для production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

try:
    from .local import *
except ImportError:
    pass