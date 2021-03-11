import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Py-Trading", # Replace with your own username
    version="0.1.11c",
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
    'beautifulsoup4==4.9.3',
    'certifi==2020.12.5',
    'cffi==1.14.4',
	'chardet==4.0.0',
	'click==7.1.2',
	'cryptography==3.4.2',
	'cycler==0.10.0',
	'et-xmlfile==1.0.1',
	'Flask==1.1.2',
	'GoogleNews==1.5.5',
	'html5lib==1.15.0',
	'idna==2.10',
	'itsdangerous==1.1.0',
	'jdcal==1.4.1',
	'Jinja2==2.11.3',
	'kiwisolver==1.3.1',
	'lxml==4.6.2',
	'MarkupSafe==1.1.1',
	'matplotlib==3.3.3',
	'mplfinance==0.12.7a5',
	'numpy==1.19.5',
	'oauthlib==3.1.0',
	'openpyxl==3.0.6',
	'pandas==1.2.1',
	'Pillow==8.1.0',
	'pycparser==2.20',
	'pyOpenSSL==20.0.1',
	'pyparsing==2.4.7',
	'python-dateutil==2.8.1',
	'python-dotenv==0.15.0',
	'pytz==2020.5',
	'requests==2.25.1',
	'requests-oauthlib==1.3.0',
	'six==1.15.0',
	'td-ameritrade-python-api==0.3.4',
	'tweepy==3.10.0',
	'urllib3==1.26.2',
	'websockets==8.1',
	'Werkzeug==1.0.1',
    ]
)