#!/usr/bin/env python
from setuptools import setup, find_packages

version = '1.0'

install_requires     = []

setup(
    name                 = 'scryptoslib',
    packages             = find_packages(),
    version              = version,
    description          = "CTF library",
    author               = "scryptos",
    author_email         = "193sim@gmail.com",
    url                  = 'https://github.com/scryptos/scryptos/',
    install_requires     = install_requires,
)
