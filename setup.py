import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="threefive",
    version="2.0.59",
    author="fu-corp",
    author_email="spam@futzu.com",
    description="The SCTE 35 parser Used By Tens of People.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/threefive",
    packages=setuptools.find_packages(),
    install_requires=["bitn>=0.0.21",],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
