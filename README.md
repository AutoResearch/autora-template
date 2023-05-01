# AutoRA Template

## Quickstart Guide

Install this in an environment using your chosen package manager. In this example we are using virtualenv

Install:
- python (3.8 or greater): https://www.python.org/downloads/
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

## Add your contribution 
Your autora-subpackage should include (1) your code implementing in the respective folder of src/autora/*, 
(2) **unit tests** for your contribution in the tests folder, and (3) respective **documentation**. (4) Update the README.md file
(5) Delete all folders in src/autora that don't contain your contribution

### Adding your code implementation
Add your code implementation to src/autora/theorist, src/autora/experimentalist or src/autora/experiment_runner. You can create new categories if none of them seems fitting.

### Adding tests
You should also add tests. These can be [doctests](https://docs.python.org/3/library/doctest.html) or as test cases in `tests/test_your_contribution_name.py`. 

### Adding documentation
You may document your contribution in `docs/index.md`

## Add new dependencies 

In pyproject.toml add the new dependencies under `dependencies`

Install the added dependencies
```shell
pip install -e ".[dev]"
```

## Publishing the package

Update the meta data under `project` in the pyproject.toml file to include name, description, author-name, author-email and version.
Also, update the URL for the repository under `project.urls`.

- Follow the guide here: https://packaging.python.org/en/latest/tutorials/packaging-projects/

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