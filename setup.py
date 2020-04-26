import setuptools
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open("README.md", "r") as fh:
    long_description = fh.read()


requirements = read("requirements.txt").split()

setuptools.setup(
    name="bilucci",
    version="0.1.0",
    author="Bilal Retiat",
    author_email="bilalphilomath@gmail.com",
    description="A simple Telegram bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/philomath213/bilucci-bot",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
