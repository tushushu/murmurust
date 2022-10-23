use pyo3::prelude::*;
use std::mem;
use numpy::ndarray::{ArrayD, ArrayViewD, ArrayViewMutD};
use numpy::{IntoPyArray, PyArrayDyn, PyReadonlyArrayDyn};


#[pyfunction]
fn fmix32(hash: u32) -> u32 {
    let mut h = hash;
    h ^= h.wrapping_shr(16);
    h = h.wrapping_mul(0x85ebca6b);
    h ^= h.wrapping_shr(13);
    h = h.wrapping_mul(0xc2b2ae35);
    h ^= h.wrapping_shr(16);
    h
}

#[pyfunction]
fn fmix64(hash: u64) -> u64 {
    let mut h = hash;
    h ^= h.wrapping_shr(33);
    h = h.wrapping_mul(0xff51afd7ed558ccd);
    h ^= h.wrapping_shr(33);
    h = h.wrapping_mul(0xc4ceb9fe1a85ec53);
    h ^= h.wrapping_shr(33);
    h
}

#[pyfunction(seed = "0", signed = "false")]
fn hash32(_py: Python, key: &str, seed: u32, signed: bool) -> Py<PyAny> {
    let len = key.len();
    let bytes = key.as_bytes();
    let bytes32: &[u32] = unsafe { mem::transmute(bytes) };
    let n_blocks = len / 4;
    let mut h1 = seed;

    let c1: u32 = 0xcc9e2d51;
    let c2: u32 = 0x1b873593;
    // body
    for i in 0..n_blocks as usize {
        let mut k1 = unsafe { *bytes32.get_unchecked(i) };

        k1 = k1.wrapping_mul(c1);
        k1 = k1.wrapping_shl(15) | k1.wrapping_shr(17);
        k1 = k1.wrapping_mul(c2);

        h1 ^= k1;
        h1 = h1.wrapping_shl(13) | h1.wrapping_shr(19);
        h1 = h1.wrapping_mul(5).wrapping_add(0xe6546b64);
    }

    // Tail
    let tail_index = n_blocks * 4;
    let mut k1: u32 = 0;
    let tail_len = len & 3;

    if tail_len >= 3 {
        k1 ^= (bytes[tail_index + 2] as u32).wrapping_shl(16);
    };
    if tail_len >= 2 {
        k1 ^= (bytes[tail_index + 1] as u32).wrapping_shl(8);
    };
    if tail_len >= 1 {
        k1 ^= bytes[tail_index] as u32;
    };
    if tail_len > 0 {
        k1 = k1.wrapping_mul(c1);
        k1 = k1.wrapping_shl(15) | k1.wrapping_shr(17);
        k1 = k1.wrapping_mul(c2);
        h1 ^= k1;
    };

    // Finalization
    h1 = fmix32(h1 ^ len as u32);
    if signed {
        (h1 as i32).to_object(_py)
    } else {
        h1.to_object(_py)
    }
}

#[pyfunction(seed = "0", signed = "false")]
fn hash128_x64(_py: Python, key: &str, seed: u32, signed: bool) -> Py<PyAny> {
    let len = key.len();
    let bytes = key.as_bytes();
    let bytes64: &[u64] = unsafe { mem::transmute(bytes) };
    let n_blocks = len / 16;
    let mut h1 = seed as u64;
    let mut h2 = seed as u64;

    let c1: u64 = 0x87c37b91114253d5;
    let c2: u64 = 0x4cf5ad432745937f;

    // body
    for i in 0..n_blocks as usize {
        let mut k1: u64 = unsafe { *bytes64.get_unchecked(i) };
        let mut k2: u64 = unsafe { *bytes64.get_unchecked(i + 8) };

        k1 = k1.wrapping_mul(c1);
        k1 = k1.wrapping_shl(31) | k1.wrapping_shr(33);
        k1 = k1.wrapping_mul(c2);

        h1 ^= k1;
        h1 = h1.wrapping_shl(27) | h1.wrapping_shr(37);
        h1 = h1.wrapping_add(h2);
        h1 = h1.wrapping_mul(5).wrapping_add(0x52dce729);

        k2 = k2.wrapping_mul(c2);
        k2 = k2.wrapping_shl(33) | k2.wrapping_shr(31);
        k2 = k2.wrapping_mul(c1);

        h2 ^= k2;
        h2 = h2.wrapping_shl(31) | h2.wrapping_shr(33);
        h2 = h1.wrapping_add(h2);
        h2 = h2.wrapping_mul(5).wrapping_add(0x38495ab5);
    }
    // tail
    let tail_index = n_blocks * 16;
    let mut k1: u64 = 0;
    let mut k2: u64 = 0;
    let tail_len = len & 15;

    if tail_len >= 15 {
        k2 ^= (bytes[tail_index + 14] as u64).wrapping_shl(48);
    };
    if tail_len >= 14 {
        k2 ^= (bytes[tail_index + 13] as u64).wrapping_shl(40);
    };
    if tail_len >= 13 {
        k2 ^= (bytes[tail_index + 12] as u64).wrapping_shl(32);
    };
    if tail_len >= 12 {
        k2 ^= (bytes[tail_index + 11] as u64).wrapping_shl(24);
    };
    if tail_len >= 11 {
        k2 ^= (bytes[tail_index + 10] as u64).wrapping_shl(16);
    };
    if tail_len >= 10 {
        k2 ^= (bytes[tail_index + 9] as u64).wrapping_shl(8);
    };
    if tail_len >= 9 {
        k2 ^= bytes[tail_index + 8] as u64;
    };

    if tail_len > 8 {
        k2 = k2.wrapping_mul(c2);
        k2 = k2.wrapping_shl(33) | k2.wrapping_shr(31);
        k2 = k2.wrapping_mul(c1);
        h2 ^= k2;
    };

    if tail_len >= 8 {
        k1 ^= (bytes[tail_index + 7] as u64).wrapping_shl(56);
    };
    if tail_len >= 7 {
        k1 ^= (bytes[tail_index + 6] as u64).wrapping_shl(48);
    };
    if tail_len >= 6 {
        k1 ^= (bytes[tail_index + 5] as u64).wrapping_shl(40);
    };
    if tail_len >= 5 {
        k1 ^= (bytes[tail_index + 4] as u64).wrapping_shl(32);
    };
    if tail_len >= 4 {
        k1 ^= (bytes[tail_index + 3] as u64).wrapping_shl(24);
    };
    if tail_len >= 3 {
        k1 ^= (bytes[tail_index + 2] as u64).wrapping_shl(16);
    };
    if tail_len >= 2 {
        k1 ^= (bytes[tail_index + 1] as u64).wrapping_shl(8);
    };
    if tail_len >= 1 {
        k1 ^= bytes[tail_index] as u64;
    };
    if tail_len > 0 {
        k1 = k1.wrapping_mul(c1);
        k1 = k1.wrapping_shl(31) | k1.wrapping_shr(33);
        k1 = k1.wrapping_mul(c2);
        h1 ^= k1;
    };

    h1 ^= len as u64;
    h2 ^= len as u64;

    h1 = h1.wrapping_add(h2);
    h2 = h1.wrapping_add(h2);

    h1 = fmix64(h1);
    h2 = fmix64(h2);

    h1 = h1.wrapping_add(h2);
    h2 = h1.wrapping_add(h2);

    let result = (h2 as u128).wrapping_shl(64) | h1 as u128;

    if signed {
        (result as i128).to_object(_py)
    } else {
        result.to_object(_py)
    }
}

#[pyfunction(seed = "0", signed = "false")]
fn hash_numpy(_py: Python, keys: ArrayViewD<'_, &str>, seed: u32, signed: bool) -> ArrayD<u32> {
    0

#[pymodule]
fn mmr3(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fmix32, m)?)?;
    m.add_function(wrap_pyfunction!(fmix64, m)?)?;
    m.add_function(wrap_pyfunction!(hash32, m)?)?;
    m.add_function(wrap_pyfunction!(hash128_x64, m)?)?;

    Ok(())
}
