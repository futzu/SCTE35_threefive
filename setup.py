#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

with open("threefive/version.py","r", encoding="utf-8") as latest:
    version = latest.read().split("'")[1]

setuptools.setup(
    name="threefive",
    version=version,
    author="Adrian and a Cast of Thousands.",
    author_email="spam@iodisco.com",
    description="The Undisputed Heavyweight Champion of SCTE-35.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/threefive",
    install_requires=[
        'new_reader >= 0.1.7',
        "pyaes",
    ],

    scripts=['bin/threefive'],
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.6",
)
