# GeoDataKit
Python tools for geoscience data analysis and visualisation

NB: this is really preliminary developments

## Installation
```
pip install -i https://test.pypi.org/simple/ GeoDataKit
```

## Demo
See in the notebook directory.

## Dev
Building distribution:
```
python setup.py sdist bdist_wheel
```

Pushing to PYPI:
```
twine upload -r pypitest --verbose -p ######## dist/*
```

