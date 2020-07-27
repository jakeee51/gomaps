import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = "gmapss",
    version = "0.1.0",
    author = "David J. Morfe",
    author_email = "jakemorfe@gmail.com",
    license = "MIT",
    description = "A module that queries google maps & returns the website data",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jakeee51/gmapss",
    packages = setuptools.find_packages(),
    py_modules = ["gmapss"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"]
)
