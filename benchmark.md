### How do we benchmark?

This benchmarking task is run by Github actions on ubuntu-latest. This document may be updated if a new version is released.

For each function like ``hash32``, ``hash64`` and ``hash128``, there would be some sub-tasks to compare the performances between ``mmr3`` and ``mmh3``. There are 5 rounds for each sub-task with different string sizes and number of runs:

- XS - string length 1, run 1M times;
- S - string length 10, run 1M times;
- M - string length 100, run 100K times;
- L - string length 1k, run 100K times;
- XL - string length 10k, run 100K times.

and the result of each round and the average result are both recorded.


### What does the result mean?
The benchmark score would be displayed as a markdown table similar to below:

| Item    | XS   | S    | M    | L    | XL   | Average | Faster |
| ------- | ---- | ---- | ---- | ---- | ---- | ------- | ------ |
| Hash32  | 2.0x | 2.0x | 1.7x | 0.8x | 0.5x | 1.4x    | Y      |
| Hash128 | 4.8x | 6.2x | 7.4x | 6.4x | 7.3x | 6.4x    | Y      |

Item - The task to compare the performances.
Faster - The benchmark result.

Take the 2nd line for example, it means by running the task
Hash128, the mmr3's speed is 6.4 times of mmh3 on average.


### Benchmark score
[Job link](https://github.com/tushushu/murmurust/actions/workflows/benchmark.yml)  

Info:  
************************************************************
Date: 2022-08-21 09:47:07   
System OS: Linux   
CPU:  Intel(R) Xeon(R) Platinum 8171M CPU @ 2.60GHz   
Python version: 3.10.6   
mmr3 version: 1.3.0   
mmh3 version: 3.0.0   
************************************************************

Result:

| Item    | XS   | S    | M    | L    | XL   | Average | Faster |
| ------- | ---- | ---- | ---- | ---- | ---- | ------- | ------ |
| Hash32  | 1.9x | 1.8x | 1.8x | 1.3x | 1.0x | 1.6x    | Y      |
| Hash128 | 1.9x | 1.9x | 1.8x | 1.5x | 1.0x | 1.6x    | Y      |

2 of 2 tasks are faster!
