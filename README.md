# pylint-pydantic
A Pylint plugin to help Pylint understand the Pydantic

### How to use

#### in console
```
git clone https://github.com/fcfangcc/pylint-pydantic.git
cd pylint-pydantic
python setup.py install
pylint --load-plugins pylint_pydantic xxxxx
```
#### in vscode
settings.json add item.
```
    "python.linting.pylintArgs": [
        "--load-plugins pylint_pydantic"
    ]
```

### Tests
```
pylint --rcfile=pylintrc --load-plugins pylint_pydantic examples/base_model.py

------------------------------------
Your code has been rated at 10.00/10
```