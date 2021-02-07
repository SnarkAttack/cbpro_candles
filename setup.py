import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cbpro_candles", # Replace with your own username
    version="0.0.1",
    author="Patrick McQuay",
    author_email="patrick.mcquay@gmail.com",
    description="Package to build and track candles for CoinbasePro",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'cbpro',
        'python-dateutil'
    ],
    python_requires='>=3.6',
)