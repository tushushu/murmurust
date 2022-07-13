use pyo3::prelude::*;

#[pyfunction]
fn finalize(hash: u32) -> u32 {
    let mut h = hash;
    h ^= h.wrapping_shr(16);
    h = h.wrapping_mul(0x85ebca6b);
    h ^= h.wrapping_shr(13);
    h = h.wrapping_mul(0xc2b2ae35);
    h ^= h.wrapping_shr(16);
    h
}

#[pymodule]
fn mmr3(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(finalize, m)?)?;

    Ok(())
}
