from setuptools import setup, find_packages

setup(
    name='pocketbook',
    version='0.0.1',
    description='Command line wallet application',
    url='https://github.com/fetch/',
    author='Edward FitzGerald',
    author_email='edward.fitzgerald@fetch.ai',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['fetch-ledger-api', 'toml'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage', 'pytest'],
    },
    entry_points={
        'console_scripts': [
            'pocketbook=pocketbook.cli:main'
        ],
    },
)
