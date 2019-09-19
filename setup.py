from setuptools import setup


requires = [
    'psycopg2',
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
