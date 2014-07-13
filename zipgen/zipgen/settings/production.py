from zipgen.settings.base import *

DEBUG = False

ADMINS = (
    ('Foo Bar', 'foo@bar.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'zipdb.production.sqlite', # different name to dev
    }
}

MANAGERS = ADMINS
