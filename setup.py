#!/usr/bin/env python

"""The setup script."""

import os
import sys
from setuptools import setup, find_packages

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

VERSIONFILE = os.path.join(THIS_DIR, "codintxt", "__init__.py")
VERSION = None
for line in open(VERSIONFILE, "r").readlines():
    if line.startswith("__version__"):
        VERSION = line.split('"')[1]

if not VERSION:
    raise RuntimeError("No version defined in codintxt.__init__.py")


with open("requirements.txt") as f:
    required = f.read().splitlines()


if sys.argv[-1].startswith("publish"):
    if os.system("pip list | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    if os.system("pip list | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    if sys.argv[-1] == "publishtest":
        os.system("twine upload -r test dist/*")
    else:
        os.system("twine upload dist/*")
        print("You probably want to also tag the version now:")
        print("  git tag -a {0} -m 'version {0}'".format(VERSION))
        print("  git push --tags")
    sys.exit()


with open("README.md") as readme_file:
    readme = readme_file.read()


setup(
    author="Konstantinos Panayiotou",
    author_email="klpanagi@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="",
    license="MIT license",
    long_description=readme,
    package_data={"": ["*.tx"]},
    keywords="codintxt",
    name="codintxt",
    packages=find_packages(include=["codintxt", "codintxt.*"]),
    install_requires=required,
    test_suite="tests",
    url="https://github.com/robotics-4-all/codintxt",
    version=VERSION,
    zip_safe=False,
)
