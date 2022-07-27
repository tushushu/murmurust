from typing import Any, Dict, Optional

import mmh3
import pytest
from mmr3 import fmix32, fmix64, hash32


def _fmix32(hash: int) -> int:
    hash ^= hash >> 16
    hash = (hash * 0x85ebca6b) & 0xFFFFFFFF
    hash ^= hash >> 13
    hash = (hash * 0xc2b2ae35) & 0xFFFFFFFF
    hash ^= hash >> 16
    return hash


def _fmix64(hash: int) -> int:
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


def _hash32(key: str, seed: int, signed: bool) -> int:
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
    if signed:
        if result & 0x80000000 == 0:
            return result
        else:
            return -((result ^ 0xFFFFFFFF) + 1)
    return result


@pytest.mark.parametrize(
    'key, seed, signed',
    [
        # key not None
        ('foo', None, None),
        ('bar', None, None),
        ('baz', None, None),

        # signed is None
        ('foo', 0, None),
        ('foo', 100, None),

        # seed is None
        ('foo', None, False),
        ('foo', None, True),

        # All not None
        ('foo', 0, False),
        ('foo', 0, True),
        ('foo', 100, False),
        ('foo', 100, True),
        ('bar', 0, False),
        ('bar', 0, True),
        ('bar', 100, False),
        ('bar', 100, True),
        ('baz', 0, False),
        ('baz', 0, True),
        ('baz', 100, False),
        ('baz', 100, True),
    ],
)
def test_hash2(
    key: str,
    seed: Optional[int],
    signed: Optional[bool],
) -> None:
    kwargs: Dict[str, Any] = {"key": key}
    if seed is None:
        seed = 0
    else:
        kwargs["seed"] = seed
    if signed is None:
        signed = False
    else:
        kwargs["signed"] = signed
    result = hash32(**kwargs)
    assert result == _hash32(key, seed, signed)
    assert result == mmh3.hash(key, seed, signed)
