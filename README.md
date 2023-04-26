# AutoRA Theorist Template

## How to Develop

Install this in an environment using your chosen package manager. 

### Using `virtualenv`

Install:
- python: https://www.python.org/downloads/
- virtualenv: https://virtualenv.pypa.io/en/latest/installation.html

Create a new virtual environment:
```shell
virtualenv venv
```

Activate it:
```shell
source venv/bin/activate
```

Use `pip install` to install the current project (`"."`) in editable mode (`-e`) with dev-dependencies (`[dev]`):
```shell
pip install -e ".[dev]"
```

Build the package using:
```shell
python -m build
```

Publish the package to PyPI using `twine`:
```shell
twine upload dist/* 
```

## Workflows
...