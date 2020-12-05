import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="cs147dvparser",
    version="1.2.0",
    author="Richard DeAmicis, Jordan Conragan",
    author_email="rtdeamicis@gmail.com, jordanvonpordan@gmail.com",
    description="converts CS147DV assembly language instructions into hexadecimal code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://rdeamici.github.io/CS147DVParser/",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts":['cs147DVParser = AssemblyParser.AssemblyParser:main']
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Java",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls = {
        'Source': 'https://github.com/rdeamici/CS147DVParser/tree/master/CS147DVPyParser'   
    }
)