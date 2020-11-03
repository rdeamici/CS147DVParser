import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="CS147DVPyParser-rdeamicis",
    version="0.0.1",
    author="Richard DeAmicis",
    author_email="rtdeamicis@gmail.com",
    description="A package for converting CS147DV assembly language instructions into hexadecimal code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rdeamici/CS147DVParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Java",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)