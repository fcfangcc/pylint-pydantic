from setuptools import setup

LONG_DESCRIPTION = open("README.rst").read()
with open("./requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setup(
    name="pylint-pydantic",
    version="0.4.1",
    description="A Pylint plugin to help Pylint understand the Pydantic",
    long_description=LONG_DESCRIPTION,
    author="fcfangcc",
    author_email="swjfc22@163.com",
    url="https://github.com/fcfangcc/pylint-pydantic",
    packages=["pylint_pydantic"],
    license="GPLv3",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    keywords=["pylint", "pydantic"],
    python_requires=">=3.10",
    install_requires=install_requires,
)
