from setuptools import find_packages, setup

setup(
    name="bootpy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.5.2",
        "jinja2>=3.1.2",
    ],
    entry_points={
        "console_scripts": [
            "bootpy=bootpy.cli:app",
        ],
    },
)
