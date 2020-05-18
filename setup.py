import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Piscord",
    version="1.3.0",
    author="Astremy",
    description="Piscord is a python framework to communicate with the Discord api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Astremy/Piscord",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
