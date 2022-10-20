from .mmr3 import fmix32, fmix64, hash32, hash128_x64  # noqa:F401

__version__ = "1.3.1"


def hash(bit: int, key: str, seed: int = 0, signed: bool = False) -> int:
    if bit == 32:
        return hash32(key=key, seed=seed, signed=signed)
    elif bit == 128:
        return hash128_x64(key=key, seed=seed, signed=signed)
    else:
        raise ValueError("Parameter bit should be either 32 or 128!")
