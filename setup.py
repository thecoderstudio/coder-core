from setuptools import setup

requires = [
    'alembic',
    'bcrypt',
    'bleach',
    'psycopg2',
    'pycrypto',
    'pyramid',
    'marshmallow',
    'sqlalchemy',
    'zope.sqlalchemy'
]

setup(
    name='codercore',
    version='1.0.0',
    description='codercore',
    author="Code R",
    author_email='hello@coderstudio.nl',
    test_suite='codercore',
    install_requires=requires
)
