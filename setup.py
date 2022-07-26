import distutils.spawn
import os
import re
import shlex
import subprocess
import sys

from setuptools import find_packages, setup


def get_version():
    filename = "trainme/__init__.py"
    with open(filename) as f:
        match = re.search(
            r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M
        )
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


def get_install_requires():
    install_requires = [
        "imgviz>=0.11",
        "matplotlib<3.3",  # for PyInstaller
        "natsort>=7.1.0",
        "numpy",
        "Pillow>=2.8",
        "PyYAML",
        "qtpy!=1.11.2",
        "termcolor",
    ]

    # Find python binding for qt with priority:
    # PyQt5 -> PySide2
    # and PyQt5 is automatically installed on Python3.
    QT_BINDING = None

    try:
        import PyQt5  # noqa # pylint: disable=unused-import

        QT_BINDING = "pyqt5"
    except ImportError:
        pass

    if QT_BINDING is None:
        try:
            import PySide2  # noqa # pylint: disable=unused-import

            QT_BINDING = "pyside2"
        except ImportError:
            pass

    if QT_BINDING is None:
        # PyQt5 can be installed via pip for Python3
        # 5.15.3, 5.15.4 won't work with PyInstaller
        install_requires.append("PyQt5!=5.15.3,!=5.15.4")
        QT_BINDING = "pyqt5"

    del QT_BINDING

    if os.name == "nt":  # Windows
        install_requires.append("colorama")

    return install_requires


def get_long_description():
    with open("README.md") as f:
        long_description = f.read()
    try:
        # when this package is being released
        import github2pypi

        return github2pypi.replace_url(
            slug="vietanhdev/trainme", content=long_description, branch="main"
        )
    except ImportError:
        # when this package is being installed
        return long_description


def main():
    version = get_version()

    if sys.argv[1] == "release":
        try:
            import github2pypi  # noqa # pylint: disable=unused-import
        except ImportError:
            print(
                "Please install github2pypi\n\n\tpip install github2pypi\n",
                file=sys.stderr,
            )
            sys.exit(1)

        if not distutils.spawn.find_executable("twine"):
            print(
                "Please install twine:\n\n\tpip install twine\n",
                file=sys.stderr,
            )
            sys.exit(1)

        commands = [
            "git push origin main",
            f"git tag v{version}",
            "git push origin --tags",
            "python setup.py sdist",
            f"twine upload dist/trainme-{version}.tar.gz",
        ]
        for cmd in commands:
            print(f"+ {cmd}")
            subprocess.check_call(shlex.split(cmd))
        sys.exit(0)

    setup(
        name="trainme",
        version=version,
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
        package_data={
            "trainme": [
                "trainme/widgets/labeling/labelme/icons/*",
                "trainme/configs/*.yaml",
            ]
        },
    )


if __name__ == "__main__":
    main()