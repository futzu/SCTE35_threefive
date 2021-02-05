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
    description="threefive is the best SCTE-35 Parsing Lib I have ever seen. I'm not just saying that because I wrote threefive, I'm saying it because it's true. Can threefive parse Mpegts video for SCTE35? Yes Ma'am.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/SCTE35-threefive",
    packages=setuptools.find_packages(),
    install_requires=["bitn>=0.0.37",],
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
