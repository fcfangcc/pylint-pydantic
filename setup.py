from setuptools import setup
LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='pylint-pydantic',
    version='0.1.1',
    description='A Pylint plugin to help Pylint understand the Pydantic',
    long_description=LONG_DESCRIPTION,
    author='fcfangcc',
    author_email='swjfc22@163.com',
    url='https://github.com/fcfangcc/pylint-pydantic',
    packages=['pylint_pydantic'],
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python :: 3.9',
    ],
    keywords=['pylint', 'pydantic'],
    python_requires=">=3.9"
)
