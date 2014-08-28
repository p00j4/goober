#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
from setuptools import setup, find_packages

setup(
    name = "goober",
    version = "0.1.3",
    packages = find_packages(),
    description = "List tests with errors/failures after a multiprocess nosetest run.",
    author = "Dustin Keitel",
    license = "MIT",
    url = "https://github.com/dustinkeitel/goober",
    install_requires = ['nose'],
    py_modules = ['goober'],
    entry_points = {
        'nose.plugins.0.10': [
            'goober = goober:Goober'
            ]
        },

)