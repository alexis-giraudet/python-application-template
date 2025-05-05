# Python application template

## Overview

```
.
├── LICENSE
├── pyproject.toml
├── README.md
├── src
│   ├── demo_textual.py
│   ├── hello_world.py
│   └── pyvisapp
│       ├── app.py
│       ├── __init__.py
│       └── style.tcss
└── tests
    └── test_demo.py
```

## Getting started

[Creating a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)

## Setup

[Creation of virtual environments](https://docs.python.org/3/library/venv.html)

### Debian/Ubuntu

Install system dependencies, create/activate a Python virtual environment and install Python dependencies:
```sh
sudo apt update
sudo apt install python3-pip python3-venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip build whl2pyz pytest
```

## Develop

[Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial)
[Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python)

Install the application and make it editable (you don't have to reinstall it each time you edit the code):
```sh
python3 -m install --editable .
```

## Test

Run the tests:
```sh
pytest
```

## Build

Build source and wheel packages:
```sh
python3 -m build
```

Build portable zip app (output to ./bin folder):
```sh
whl2pyz --python "/usr/bin/env python3" --compress dist/*.whl
```

## Publish

### GitHub

### PyPI

## Reading
 - [Python Packaging User Guide](https://packaging.python.org/en/latest/#)
 - [setuptools](https://setuptools.pypa.io/en/latest/#)
 - [A Comprehensive Guide to Python Project Management and Packaging: Concepts Illustrated with uv – Part I](https://reinforcedknowledge.com/a-comprehensive-guide-to-python-project-management-and-packaging-concepts-illustrated-with-uv-part-i/)
 - [pytest](https://docs.pytest.org/en/stable/#)
 - [PEP Index](https://peps.python.org/#)
 - [Black](https://black.readthedocs.io/en/stable/)
