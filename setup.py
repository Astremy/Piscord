import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements.txt", "r") as file:
    requires = file.read()

setuptools.setup(
    name="piscord",
    version="1.5.0",
    author="Astremy",
    description="Piscord is a python framework to communicate with the Discord api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Astremy/Piscord",
    packages=["piscord"],
    license="LICENSE",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requires.splitlines(),
)