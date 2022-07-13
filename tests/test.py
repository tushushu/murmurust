import pytest
from mmr3 import finalize


def fmix(h):
    h ^= h >> 16
    h = (h * 0x85ebca6b) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 0xc2b2ae35) & 0xFFFFFFFF
    h ^= h >> 16
    return h


@pytest.mark.parametrize(
    'hash',
    [0, 1, 2, 3, 5],
)
def test_finalize(hash: int) -> None:
    assert finalize(hash) == fmix(hash)
