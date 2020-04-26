import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
