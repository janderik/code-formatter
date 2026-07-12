from setuptools import setup, find_packages

setup(
    name="code-formatter",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "fmt=cli:main",
        ],
    },
    author="janderik",
    description="Multi-language code formatter",
    python_requires=">=3.8",
)
