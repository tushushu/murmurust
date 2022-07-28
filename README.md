# murmurust
[![PyPI](https://img.shields.io/pypi/v/mmr3)](https://pypi.org/project/mmr3/)
[![License](https://img.shields.io/github/license/tushushu/murmurust)](https://github.com/tushushu/murmurust/blob/main/LICENSE)
[![CI](https://github.com/tushushu/murmurust/workflows/CI/badge.svg)](https://github.com/tushushu/murmurust/workflows/main.yml)
[![publish](https://github.com/tushushu/murmurust/workflows/publish/badge.svg)](https://github.com/tushushu/murmurust/actions/workflows/publish.yml)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-blue)](https://github.com/PyCQA/flake8)
[![downloads/month](https://static.pepy.tech/badge/mmr3/month)](https://pypi.org/project/mmr3/)  


## What
Python binding of MurmurHash3 Rust implementation.


## Requirements
-  Python: 3.8+
-  OS: Linux, MacOS and Windows


## Installation
Run `pip install mmr3`


## Examples
```Python
>>> import mmr3
# By default, seed=0, return unsigned int.
>>> mmr3.hash32('foo')
4138058784

# When seed = 100.
>>> mmr3.hash32('foo', seed=100)
3757588558

# Return signed int.
>>> mmr3.hash32('foo', signed=True)
-156908512
```
