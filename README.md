
[![SWH](https://archive.softwareheritage.org/badge/origin/https://github.com/GeoISTO/GeoDataKit/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/GeoISTO/GeoDataKit)
[![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:e0c58ecf5a7bdfc54d6f8b67cc8ef25595ba4ee0/)](https://archive.softwareheritage.org/swh:1:dir:e0c58ecf5a7bdfc54d6f8b67cc8ef25595ba4ee0;origin=https://github.com/GeoISTO/GeoDataKit;visit=swh:1:snp:473d154fffc3460a153485d06c155d4c373fb97f;anchor=swh:1:rev:a0fbe4c73e77b454a7669c69102ca677e5ffd53c)

# GeoDataKit
Python tools for geoscience data analysis and visualisation

## Publications

Please reference this code if used in any publication:

Gautier Laurent. GeoDataKit. 2025, ⟨swh:1:snp:473d154fffc3460a153485d06c155d4c373fb97f;origin=https://github.com/GeoISTO/GeoDataKit⟩. ⟨hal-05168282⟩

Papers refering to GeoDataKit:
* Pereira et al. (2024) [⟨10.5194/ejm-36-491-2024⟩](https://dx.doi.org/10.5194/ejm-36-491-2024)

## Demo
Demonstration Notebooks are available in the [./notebook](./notebook) directory.

Available notebooks:
1. Rose Diagram demo
2. Hough Transform demo
3. Principal Component and Linear Discriminant Analysis PCA and LDA


## Installation
```
pip install  GeoDataKit
```


## Dev
Building distribution:
```
python setup.py sdist bdist_wheel
```

Pushing to PYPI:
```
twine upload --verbose dist/*
```

