import pytest
from mmr3 import fmix32, fmix64, hash32


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


def _hash32(key: str, seed: int):
    data = key.encode()
    length = len(data)
    n_blocks = int(length / 4)

    h1 = seed
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    # body
    for i in range(0, n_blocks * 4, 4):
        k1 = data[i + 3] << 24 | \
            data[i + 2] << 16 | \
            data[i + 1] << 8 | \
            data[i]

        k1 = (c1 * k1) & 0xFFFFFFFF
        k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF
        k1 = (c2 * k1) & 0xFFFFFFFF

        h1 ^= k1
        h1 = (h1 << 13 | h1 >> 19) & 0xFFFFFFFF
        h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

    # Tail
    tail_index = n_blocks * 4
    k1 = 0
    tail_size = length & 3

    if tail_size >= 3:
        k1 ^= data[tail_index + 2] << 16
    if tail_size >= 2:
        k1 ^= data[tail_index + 1] << 8
    if tail_size >= 1:
        k1 ^= data[tail_index]

    if tail_size > 0:
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    # Finalization
    result = _fmix32(h1 ^ length)
    return result


@pytest.mark.parametrize(
    'key, seed',
    [
        ('foo', 0),
        ('foo', 100),
        ('bar', 0),
        ('baz', 0),
    ],
)
def test_mmh3_32(key: str, seed: int) -> None:
    assert hash32(key, seed) == _hash32(key, seed)
