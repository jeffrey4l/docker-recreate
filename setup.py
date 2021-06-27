#!/bin/bash

from setuptools import setup


setup(
    name='docker-recreate',
    version='1.0.2',
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
