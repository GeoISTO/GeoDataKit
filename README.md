# GeoDataKit
Python tools for geoscience data analysis and visualisation

NB: this is really preliminary developments

## Demo
Demonstration Notebooks are available in the [./notebook](./notebook) directory.

Available notebooks:
1. Rose Diagram demo
2. Hough Transform demo


## Installation
```
pip install -i https://test.pypi.org/simple/ GeoDataKit
```


## Dev
Building distribution:
```
python setup.py sdist bdist_wheel
```

Pushing to PYPI:
```
twine upload -r pypitest --verbose -p ######## dist/*
```

