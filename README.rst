pylint-pydantic
================
A Pylint plugin to help Pylint understand the Pydantic

How to use
===============
Installation

.. code:: shell

    pip install pylint-pydantic

Use in console

.. code:: shell

    pylint --load-plugins pylint_pydantic xxxxx

Use in vscode,settings.json add item

.. code:: shell

    "python.linting.pylintArgs": ["--load-plugins", "pylint_pydantic"]

Tests
============
.. code:: shell

    pylint --rcfile=pylintrc --load-plugins pylint_pydantic tests/base_model.py
    ------------------------------------
    Your code has been rated at 10.00/10

FAQ
=====================
- How to resolve `pylint: No name 'BaseModel' in module 'pydantic'`?
    Add `--extension-pkg-whitelist='pydantic'` parameter (see `#1961 <https://github.com/samuelcolvin/pydantic/issues/1961>`_)

Other
=====================
If you have any questions, please create a issue.
https://github.com/fcfangcc/pylint-pydantic/issues


Changelog
=====================
- v0.2.0: support Pydantic V2
- v0.2.1: support `model_validator`
- v0.2.2: fix model_validator keyword **mode**, pydatic>=2.0.3
- v0.2.4: fix pydantic.Field with BaseModel support