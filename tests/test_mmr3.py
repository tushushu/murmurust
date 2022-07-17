import pytest
from mmr3 import fmix32, fmix64


def _fmix32(hash):
    hash ^= hash >> 16
    hash = (hash * 0x85ebca6b) & 0xFFFFFFFF
    hash ^= hash >> 13
    hash = (hash * 0xc2b2ae35) & 0xFFFFFFFF
    hash ^= hash >> 16
    return hash


def _fmix64(hash):
    hash ^= hash >> 33
    hash = (hash * 0xff51afd7ed558ccd) & 0xFFFFFFFFFFFFFFFF
    hash ^= hash >> 33
    hash = (hash * 0xc4ceb9fe1a85ec53) & 0xFFFFFFFFFFFFFFFF
    hash ^= hash >> 33
    return hash


@pytest.mark.parametrize(
    'hash',
    [0, 1, 2, 3, 5],
)
def test_fmix32(hash: int) -> None:
    assert fmix32(hash) == _fmix32(hash)


@pytest.mark.parametrize(
    'hash',
    [0, 1, 2, 3, 5],
)
def test_fmix64(hash: int) -> None:
    assert fmix64(hash) == _fmix64(hash)
