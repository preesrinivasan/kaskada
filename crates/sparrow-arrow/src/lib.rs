#![warn(
    rust_2018_idioms,
    nonstandard_style,
    future_incompatible,
    clippy::mod_module_files,
    clippy::print_stdout,
    clippy::print_stderr,
    clippy::undocumented_unsafe_blocks
)]
pub mod attachments;
#[cfg(feature = "avro")]
pub mod avro;
mod batch;
pub mod downcast;
mod row_time;
pub mod scalar_value;
pub mod serde;
#[cfg(any(test, feature = "testing"))]
mod testing;
pub mod utils;

pub use batch::*;
pub use row_time::*;
