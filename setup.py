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


setup(
    name='docker-recreate',
    version=get_version(),
    description='Get docker run command from container',
    long_description='file:README.md',
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
