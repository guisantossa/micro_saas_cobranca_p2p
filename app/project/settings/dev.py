import os  # noqa: F401

import environ

from .base import *  # noqa: F401 F403

env = environ.Env()
environ.Env.read_env()


DEBUG = True
ALLOWED_HOSTS = ["*"]
