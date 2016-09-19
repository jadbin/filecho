# coding=utf-8

import os
import re
import sys
from setuptools import setup, find_packages

with open("README.rst") as fd:
    long_description = fd.read()


def read_version():
    p = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                     "filecho",
                     "version.py")
    with open(p, "rb") as f:
        return re.findall(r'__version__ = "([^"]+)"', f.read().decode("utf-8"))[0]


def main():
    if sys.version_info < (3, 5):
        raise RuntimeError("Python 3.5+ is required")
    install_requires = ["aiohttp"]
    setup(
        name="filecho",
        version=read_version(),
        url="https://github.com/jadbin/filecho",
        description="A web server for serving static files",
        long_description=long_description,
        author="jadbin.com",
        author_email="jadbin.com@hotmail.com",
        license="Apache 2",
        zip_safe=False,
        packages=find_packages(),
        include_package_data=True,
        entry_points={
            "console_scripts": ["filecho = filecho.cli:main"]
        },
        install_requires=install_requires,
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Topic :: Internet :: WWW/HTTP",
        ],
    )


if __name__ == "__main__":
    main()
