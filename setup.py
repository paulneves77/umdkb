#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="umdkb",
    version=0.1,
    author="Brendan Van Hook",
    author_email="brendan@vastactive.com",
    description="Control UMD's Watt balance.",
    license="ISC",
    packages=find_packages(),
    install_requires=["appdirs"],
    entry_points={"console_scripts": ["umdkb = umdkb.cli:cli"]},
)
