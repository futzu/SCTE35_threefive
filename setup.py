#!/usr/bin/env python3

import setuptools
import threefive

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="threefive",
    version=threefive.version(),
    author="fu-corp",
    author_email="spam@futzu.com",
    description="threefive Might be The Leading SCTE-35 Parsing Lib for Mpeg-TS Video Streams, and Base64 or Hex Encoded Messages. threefive is Used in Production by Some of The Largest Broadcast Networks in The World, Maybe",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/SCTE35-threefive",
    packages=setuptools.find_packages(),
    install_requires=["bitn>=0.0.33",],
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
