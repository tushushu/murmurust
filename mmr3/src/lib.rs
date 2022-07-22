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

#[pymodule]
fn mmr3(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fmix32, m)?)?;
    m.add_function(wrap_pyfunction!(fmix64, m)?)?;

    Ok(())
}
