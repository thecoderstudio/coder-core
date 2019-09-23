from setuptools import setup

requires = [
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
    version='0.1.0',
    description='codercore',
    author="Code R",
    author_email='hello@coderstudio.nl',
    install_requires=requires
)
