import os  # noqa: F401

import environ

from .base import *  # noqa: F401 F403

env = environ.Env()

if os.environ.get("ENV") != "production":
    environ.Env.read_env()

DEBUG = True


ALLOWED_HOSTS = ["cobraii.com.br", "api.cobraii.com.br", "*"]  # ajuste conforme domínio

# Segurança básica
# SECURE_HSTS_SECONDS = 3600
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
