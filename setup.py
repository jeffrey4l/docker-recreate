#!/bin/bash

from setuptools import setup
import subprocess


def get_version():
    output = subprocess.check_output(['git', 'describe', '--tags'])
    output = output.decode('utf8')
    return output.strip()


setup(
    name='docker-recreate',
    version=get_version(),
    description='Get docker run command from container',
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
