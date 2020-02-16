from io import open
from os import path

from setuptools import setup, find_packages

from pocketbook import __version__

project_root = path.dirname(__file__)

with open(path.join(project_root, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pocketbook',
    version=__version__,
    description='Command line wallet application for the Fetch.ai network',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',
    url='https://github.com/fetchai/tools-pocketbook',
    author='Edward FitzGerald',
    author_email='edward.fitzgerald@fetch.ai',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='~=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'fetchai-ledger-api==1.0.1',
        'toml',
        'colored',
    ],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage', 'pytest', 'flake8'],
    },
    entry_points={
        'console_scripts': [
            'pocketbook=pocketbook.cli:main'
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/fetchai/tools-pocketbook/issues',
        'Source': 'https://github.com/fetchai/tools-pocketbook',
    },
)
