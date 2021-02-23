#!/usr/bin/env python3

import setuptools
import threefive

with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="threefive",
    version=threefive.version(),
    author="fu-corp",
    beauthor_email="spam@so.slo.me",
    description="threefive is SCTE35 for the civilized. Can threefive parse Mpegts video for SCTE35? Yes it can.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/SCTE35-threefive",
    packages=setuptools.find_packages(),
    install_requires=["bitn>=0.0.39","crcmod",],
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
