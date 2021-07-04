#!/bin/bash

from setuptools import setup
import os
import subprocess


def get_version():
    version = os.environ.get('VERSION_NAME', None)
    if version:
        return version
    output = subprocess.check_output(['git', 'describe', '--tags'])
    output = output.decode('utf8')
    return output.strip()


def get_long_description():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='docker-recreate',
    version=get_version(),
    description='Get docker run command from container',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author='Jeffrey Zhang',
    author_email='zhang.lei.fly@gmail.com',
    url='https://www.github.com/jeffrey4l/docker-recreate',
    home_page='https://www.github.com/jeffrey4l/docker-recreate',
    entry_points={
        'console_scripts': [
            'docker-recreate=main:main'
        ]},
    py_modules=['main'],
    )
