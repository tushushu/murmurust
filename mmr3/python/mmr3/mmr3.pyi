

def fmix32(hash: int) -> int: ...


def fmix64(hash: int) -> int: ...


def hash32(
    key: str,
    seed: int = 0,
    signed: bool = False
) -> int: ...


def hash128_x64(
    key: str,
    seed: int = 0,
    signed: bool = False
) -> int: ...
