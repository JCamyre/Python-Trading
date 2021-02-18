import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Python-Trading", # Replace with your own username
    version="0.0.1",
    author="Joseph Camyre",
    author_email="jwcamry03@gmail.com",
    description="A convenient Python module for stock information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JCamyre/Python-Trading",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)