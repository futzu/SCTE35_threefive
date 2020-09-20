import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="threefive",
    version="2.1.61",
    author="fu-corp",
    author_email="spam@futzu.com",
    description="A Fast SCTE 35 Decoder for Mpeg-TS Video, and Base64 or Hex Encoded Messages.", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/futzu/threefive",
    packages=setuptools.find_packages(),
    install_requires=["bitn>=0.0.27",],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
