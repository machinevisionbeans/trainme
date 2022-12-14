"""Setup file for trainme package"""

import os
import sys
import re
from sys import platform

from setuptools import find_packages, setup


def get_version():
    """Get package version from __init__.py file"""
    filename = "trainme/__init__.py"
    with open(filename, encoding="utf-8") as f:
        match = re.search(
            r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M
        )
    if not match:
        raise RuntimeError(f"{filename} doesn't contain __version__")
    version = match.groups()[0]
    return version


def get_install_requires():
    """Get python requirements based on context"""
    install_requires = [
        "imgviz>=0.11",
        "matplotlib<3.3",  # for PyInstaller
        "natsort>=7.1.0",
        "numpy",
        "Pillow>=2.8",
        "PyYAML",
        "termcolor",
        "pyqtgraph",
        "pandas",
        "psutil",
        "trainme-core @ git+https://github.com/vietanhdev/trainme-core"
    ]

    # Guide user to install PyQt5 on macOS
    if platform == "darwin":
        try:
            import PyQt5
        except:
            print("Please try to install PyQt5 on macOS one of following ways:\n"
                  "+ Using Conda: conda install -c conda-forge pyqt==5.15.7\n"
                  "+ Using Brew: brew install pyqt@5")
            sys.exit(1)
    else:
        install_requires.append("PyQt5>=5.15.7")

    if os.name == "nt":  # Windows
        install_requires.append("colorama")

    return install_requires


def get_long_description():
    """Read long description from README"""
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
    return long_description


setup(
    name="trainme",
    version=get_version(),
    packages=find_packages(),
    description="No-code Labeling and Training Toolkit for Computer Vision",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Viet-Anh Nguyen",
    author_email="vietanh.dev@gmail.com",
    url="https://github.com/vietanhdev/trainme",
    install_requires=get_install_requires(),
    license="GPLv3",
    keywords="Image Annotation, Machine Learning, Deep Learning",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "trainme=trainme.__main__:main",
            "trainme_app=trainme.__main__:main",
        ],
    },
)
