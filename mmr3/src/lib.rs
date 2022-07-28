use pyo3::prelude::*;

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
    let data = key.as_bytes();
    let n_blocks = len / 4;
    let mut h1 = seed;

    let c1: u32 = 0xcc9e2d51;
    let c2: u32 = 0x1b873593;

    // body
    for i in (0..n_blocks * 4).step_by(4) {
        let mut k1: u32 = (data[i + 3].wrapping_shl(24)
            | data[i + 2].wrapping_shl(16)
            | data[i + 1].wrapping_shl(8)
            | data[i]) as u32;

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
        k1 ^= (data[tail_index + 2] as u32).wrapping_shl(16);
    };
    if tail_len >= 2 {
        k1 ^= (data[tail_index + 1] as u32).wrapping_shl(8);
    };
    if tail_len >= 1 {
        k1 ^= data[tail_index] as u32;
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

#[pymodule]
fn mmr3(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fmix32, m)?)?;
    m.add_function(wrap_pyfunction!(fmix64, m)?)?;
    m.add_function(wrap_pyfunction!(hash32, m)?)?;

    Ok(())
}
