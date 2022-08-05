# murmurust
[![pypi](https://img.shields.io/pypi/v/mmr3)](https://pypi.org/project/mmr3/)
[![license](https://img.shields.io/github/license/tushushu/murmurust)](https://github.com/tushushu/murmurust/blob/main/LICENSE)
[![CI](https://github.com/tushushu/murmurust/workflows/CI/badge.svg)](https://github.com/tushushu/murmurust/workflows/main.yml)
[![publish](https://github.com/tushushu/murmurust/workflows/publish/badge.svg)](https://github.com/tushushu/murmurust/actions/workflows/publish.yml)
[![code style](https://img.shields.io/badge/code%20style-flake8-blue)](https://github.com/PyCQA/flake8)
[![downloads](https://pepy.tech/badge/mmr3)](https://pypi.org/project/mmr3/)
[![downloads/month](https://static.pepy.tech/badge/mmr3/month)](https://pypi.org/project/mmr3/)  


## What
Python binding of MurmurHash3 Rust implementation.


## Requirements
-  Python: 3.8+
-  OS: Linux, MacOS and Windows


## Installation
Run `pip install mmr3`


## Benchmark
`mmr3` is faster than `mmh3` on average, which is a popular murmurhash3 library written in C/C++ and Python. For the details, please refer to [benchmark.md](https://github.com/tushushu/murmurust/blob/main/benchmark.md).  

| Item   | XS   | S    | M    | L    | XL   | Average | Faster |
| ------ | ---- | ---- | ---- | ---- | ---- | ------- | ------ |
| Hash32 | 2.1x | 2.0x | 1.8x | 1.1x | 0.8x | 1.6x    | Y      |


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
