from setuptools import setup, find_packages

setup(
    name="ibkr_trading_app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "ib_insync>=0.9.70",
        "pandas>=1.5.0",
        "pyautogui>=0.9.53",
        "Pillow>=9.2.0",
        "python-dotenv>=0.21.0",
        "logging>=0.5.1.2",
    ],
    author="etcheah",
    description="Automated trading application for Interactive Brokers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ceteongvanness/ibkr-trading-app",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
