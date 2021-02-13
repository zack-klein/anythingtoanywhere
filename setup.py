import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="anythingtoanywhere",
    author="Zack Klein",
    author_email="klein.zachary.j@gmail.com",
    description=("Load anything anywhere!."),
    license="MIT",
    packages=[
        "anythingtoanywhere",
        "anythingtoanywhere.destinations",
        "anythingtoanywhere.sources",
    ],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    url="https://github.com/zack-klein/anythingtoanywhere",
    install_requires=requirements,
)
