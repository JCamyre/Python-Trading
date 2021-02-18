import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Py-Trading", # Replace with your own username
    version="0.0.4b1",
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
    install_requires=[
        'certifi==2020.12.5',
        'chardet==4.0.0',
        'cycler==0.10.0',
        'et-xmlfile==1.0.1',
        'idna==2.10',
        'jdcal==1.4.1',
        'kiwisolver==1.3.1',
        'matplotlib==3.3.3',
        'mplfinance==0.12.7a5',
        'numpy==1.19.5',
        'openpyxl==3.0.6',
        'pandas==1.2.1',
        'Pillow==8.1.0',
        'pyparsing==2.4.7',
        'python-dateutil==2.8.1',
        'pytz==2020.5',
        'requests==2.25.1',
        'six==1.15.0',
        'urllib3==1.26.2'
    ]
)