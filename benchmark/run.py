import gc
import platform
import random
import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from timeit import timeit
from typing import Callable, Dict, List

import mmh3
import mmr3

MAX_ITEM_LEN = 16
MAX_DTYPE_LEN = 8


@dataclass
class BenchmarkScore:
    name: str
    _scores: dict

    @property
    def scores(self) -> List[str]:
        """For the score schema please refer to `self._header` method."""
        result = [self.name]
        for v in self._scores.values():
            result.append(str(v) + 'x')
        avg = round(sum(self._scores.values()) / len(self._scores), 1)
        result.append(str(avg) + 'x')
        if avg > 1:
            result.append('Y')
        else:
            result.append('N')
        return result

    def _as_markdown(self, text: List[str], cell_sizes: List[int]) -> str:
        result = ['|']
        for t, cell_size in zip(text, cell_sizes):
            content = [' '] * cell_size
            for i in range(cell_size):
                if i == 0:
                    continue
                if i - 1 < len(t):
                    content[i] = t[i - 1]
            result.append("".join(content))
            result.append('|')
        return "".join(result)

    def _line(self, cell_sizes: List[int]) -> List[str]:
        return ['-' * (x - 2) for x in cell_sizes]

    @property
    def _header(self) -> List[str]:
        return [
            'Item',
            'XS',
            'S',
            'M',
            'L',
            'XL',
            'Average',
            'Faster'
        ]

    def display(self, show_header: bool = True) -> None:
        """
        Display the benchmark score as a markdown table similar to below:

        --------
        | Item     | XS   | S    | M    | L    | XL   | Average |
        | -------  | ---- | ---- | ---- | ---- | ---- | ------- |
        | Hash32   | 0.9x | 1.0x | 1.0x | 1.0x | 1.1x | 1.0x    |
        | Hash128  | 4.8x | 6.2x | 7.4x | 6.4x | 7.3x | 6.4x    |

        Item - The task to compare the performances.
        Sample Vol. - See `Benchmarker`.

        Take the 2nd line for example, it means by running the task
        Hash128, the mmr3's speed is 6.4 times of mmh3 on average.
        """
        cell_sizes = [max(6, len(x) + 2) for x in self._header]
        cell_sizes[0] = MAX_ITEM_LEN
        cell_sizes[1] = MAX_DTYPE_LEN

        if show_header:
            print(self._as_markdown(self._header, cell_sizes))
            line = self._line(cell_sizes)
            print(self._as_markdown(line, cell_sizes))

        print((self._as_markdown(self.scores, cell_sizes)))


class Benchmarker(ABC):
    """
    An abstract class for comparing the performance between `mmr3` and other
    framework such as `mmh3`.

    There are 5 rounds for the task with different string sizes and number of
    runs:
        XS - string length 1, run 1M times;
        S - string length 10, run 1M times;
        M - string length 100, run 100K times;
        L - string length 1k, run 100K times;
        XL - string length 10k, run 100K times.

    and the result of each round and the average result are both recorded.

    The abstract methods need to be overridden by subclass.
    """

    def __init__(self) -> None:
        super().__init__()
        self.n_runs = (1000000, 1000000, 100000, 100000, 100000)
        self.sizes = (1, 10, 100, 1000, 10000)
        assert len(self.n_runs) == len(self.cases())
        assert len(self.__class__.__name__) < MAX_ITEM_LEN

    def cases(self) -> List[str]:
        """Benchmark cases for each round."""
        s = 'abcdefghijklmnopqrstuvwxyz'
        result = []
        for size in self.sizes:
            result.append(''.join(random.choice(s) for _ in range(size)))
        return result

    @abstractmethod
    def mmr3_fn(self, key: str) -> None:
        """The mmr3 function to benchmark."""

    @abstractmethod
    def other_fn(self, key: str) -> None:
        """The other function to compare with."""

    def run(self) -> BenchmarkScore:
        """Run the benchmarking task."""
        mmr3_time_elapsed = self._run(self.mmr3_fn)
        other_time_elapsed = self._run(self.other_fn)
        scores = dict()
        for k, v in mmr3_time_elapsed.items():
            scores[k] = round(other_time_elapsed[k] / v, 1)
        return BenchmarkScore(
            name=type(self).__name__,
            _scores=scores,
        )

    def _run(self, fn: Callable) -> Dict[int, float]:
        result = dict()
        for n_run, size, key in zip(self.n_runs, self.sizes, self.cases()):
            result[size] = timeit(lambda: fn(key), number=n_run)
        return result


random.seed(100)


class Hash32(Benchmarker):
    def mmr3_fn(self, key: str) -> None:
        mmr3.hash32(key)

    def other_fn(self, key: str) -> None:
        mmh3.hash(key, signed=False)


def _get_processor_name() -> str:
    if platform.system() == "Windows":
        return platform.processor()
    elif platform.system() == "Darwin":
        command = "sysctl -n machdep.cpu.brand_string"
        return subprocess.check_output(
            command, shell=True
        ).strip().decode()
    elif platform.system() == "Linux":
        command = "cat /proc/cpuinfo | grep 'model name' | uniq"
        return subprocess.check_output(
            command, shell=True
        ).strip().decode().split(":")[1]
    return ""


def display_info() -> None:
    print("Info:  ")
    line = "*" * 60
    print(line)
    print("Date:", datetime.today().strftime("%Y-%m-%d %H:%M:%S"), "  ")
    print("System OS:", platform.system(), "  ")
    print("CPU:", _get_processor_name(), "  ")
    print("Python version:", sys.version.split()[0], "  ")

    try:
        print("mmr3 version:", mmr3.__version__, "  ")
    except:  # noqa: E722
        print("mmr3 version:", "unknown")
    print("mmh3 version:", mmh3.__version__, "  ")
    print(line)
    print()


def display_result() -> None:
    print("Result:")
    print()
    n_wins = 0
    total = 0
    benchmarkers = [Hash32]
    for cls in benchmarkers:
        result = cls().run()
        if total == 0:
            result.display()
        else:
            result.display(False)
        if result.scores[-1] == 'Y':
            n_wins += 1
        total += 1
        gc.collect()
    print()
    print(f"{n_wins} of {total} tasks are faster!")


def main() -> None:
    """
    Comparing mmr3 and mmh3 performances, show the server info and output
    the result as Markdown Table.
    """
    print("GC disabled...")
    gc.disable()
    print("Benchmarking...\n")
    display_info()
    display_result()
    print("GC enabled...")
    gc.enable()


if __name__ == "__main__":
    main()
