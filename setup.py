#!/usr/bin/env python3

import setuptools
import threefive

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="threefive",
    version=threefive.version(),
    author="Adrian Thiele, Vlad Doster, James Fining, Richard Van Dijk",
    author_email="spam@so.slo.me",
    description="Pythonic SCTE-35.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/threefive",
    install_requires=[
        "crcmod",
        "pyaes",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=3.6",
)
