#!/bin/bash

import setuptools


setuptools.setup(
    setup_requires=['pbr>=2.0.0'],
    py_modules=['main'],
    pbr=True)
