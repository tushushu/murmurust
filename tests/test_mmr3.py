import subprocess
from typing import Any, Dict, Optional

import mmh3
import pytest
from mmr3 import fmix32, fmix64, hash32, hash128_x64, hash


def _get_os_kernel_bit() -> int:
    process = subprocess.Popen(
        ['getconf', 'LONG_BIT'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, _ = process.communicate()
    return int(out)


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
    n_blocks = length // 4

    h1 = seed
    c1 = 0xcc9e2d51
    c2 = 0x1b873593

    # Body
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


def _hash128_x64(_key: str, seed: int, signed: bool) -> int:
    data = _key.encode()
    length = len(data)
    n_blocks = length // 16

    h1 = seed
    h2 = seed
    c1 = 0x87c37b91114253d5
    c2 = 0x4cf5ad432745937f

    # Body
    for i in range(0, n_blocks * 8, 8):
        k1 = data[2 * i + 7] << 56 | \
            data[2 * i + 6] << 48 | \
            data[2 * i + 5] << 40 | \
            data[2 * i + 4] << 32 | \
            data[2 * i + 3] << 24 | \
            data[2 * i + 2] << 16 | \
            data[2 * i + 1] << 8 | \
            data[2 * i]

        k2 = data[2 * i + 15] << 56 | \
            data[2 * i + 14] << 48 | \
            data[2 * i + 13] << 40 | \
            data[2 * i + 12] << 32 | \
            data[2 * i + 11] << 24 | \
            data[2 * i + 10] << 16 | \
            data[2 * i + 9] << 8 | \
            data[2 * i + 8]

        k1 = (c1 * k1) & 0xFFFFFFFFFFFFFFFF
        k1 = (k1 << 31 | k1 >> 33) & 0xFFFFFFFFFFFFFFFF
        k1 = (c2 * k1) & 0xFFFFFFFFFFFFFFFF
        h1 ^= k1

        h1 = (h1 << 27 | h1 >> 37) & 0xFFFFFFFFFFFFFFFF
        h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
        h1 = (h1 * 5 + 0x52dce729) & 0xFFFFFFFFFFFFFFFF

        k2 = (c2 * k2) & 0xFFFFFFFFFFFFFFFF
        k2 = (k2 << 33 | k2 >> 31) & 0xFFFFFFFFFFFFFFFF
        k2 = (c1 * k2) & 0xFFFFFFFFFFFFFFFF
        h2 ^= k2

        h2 = (h2 << 31 | h2 >> 33) & 0xFFFFFFFFFFFFFFFF
        h2 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
        h2 = (h2 * 5 + 0x38495ab5) & 0xFFFFFFFFFFFFFFFF

    # Tail
    tail_index = n_blocks * 16
    k1 = 0
    k2 = 0
    tail_size = length & 15

    if tail_size >= 15:
        k2 ^= data[tail_index + 14] << 48
    if tail_size >= 14:
        k2 ^= data[tail_index + 13] << 40
    if tail_size >= 13:
        k2 ^= data[tail_index + 12] << 32
    if tail_size >= 12:
        k2 ^= data[tail_index + 11] << 24
    if tail_size >= 11:
        k2 ^= data[tail_index + 10] << 16
    if tail_size >= 10:
        k2 ^= data[tail_index + 9] << 8
    if tail_size >= 9:
        k2 ^= data[tail_index + 8]

    if tail_size > 8:
        k2 = (k2 * c2) & 0xFFFFFFFFFFFFFFFF
        k2 = (k2 << 33 | k2 >> 31) & 0xFFFFFFFFFFFFFFFF
        k2 = (k2 * c1) & 0xFFFFFFFFFFFFFFFF
        h2 ^= k2

    if tail_size >= 8:
        k1 ^= data[tail_index + 7] << 56
    if tail_size >= 7:
        k1 ^= data[tail_index + 6] << 48
    if tail_size >= 6:
        k1 ^= data[tail_index + 5] << 40
    if tail_size >= 5:
        k1 ^= data[tail_index + 4] << 32
    if tail_size >= 4:
        k1 ^= data[tail_index + 3] << 24
    if tail_size >= 3:
        k1 ^= data[tail_index + 2] << 16
    if tail_size >= 2:
        k1 ^= data[tail_index + 1] << 8
    if tail_size >= 1:
        k1 ^= data[tail_index]

    if tail_size > 0:
        k1 = (k1 * c1) & 0xFFFFFFFFFFFFFFFF
        k1 = (k1 << 31 | k1 >> 33) & 0xFFFFFFFFFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFFFFFFFFFF
        h1 ^= k1

    # Finalization
    h1 ^= length
    h2 ^= length

    h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
    h2 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF

    h1 = _fmix64(h1)
    h2 = _fmix64(h2)

    h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
    h2 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF

    result = h2 << 64 | h1

    if not signed:
        return result
    else:
        if result & 0x80000000000000000000000000000000 == 0:
            return result
        else:
            return -(result ^ 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) - 1


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
def test_hash(
    key: str,
    seed: Optional[int],
    signed: Optional[bool],
) -> None:
    # hash32
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
    assert result == hash(32, **kwargs)
    assert result == _hash32(key, seed, signed)
    assert result == mmh3.hash(key=key, seed=seed, signed=signed)

    # hash128 x64
    kwargs = {"key": key}
    if seed is None:
        seed = 0
    else:
        kwargs["seed"] = seed
    if signed is None:
        signed = False
    else:
        kwargs["signed"] = signed

    result = hash128_x64(**kwargs)
    assert result == hash(128, **kwargs)
    assert result == _hash128_x64(key, seed, signed)
    assert result == mmh3.hash128(key=key, seed=seed, signed=signed)
