use crate::{Evaluator, EvaluatorFactory, RuntimeInfo, StaticInfo};
use arrow::array::ArrayRef;
use sparrow_plan::ValueRef;

/// Evaluator for the `collect` instruction.
///
/// Collect collects a stream of values into a List<T>. A list is produced
/// for each input value received, growing up to a maximum size.
#[derive(Debug)]
pub struct CollectListEvaluator {
    /// The max size of the buffer.
    ///
    /// Once the max size is reached, the front will be popped and the new
    /// value pushed to the back.
    _max: i64,
    _input: ValueRef,
    _tick: ValueRef,
    _duration: ValueRef,
}

impl EvaluatorFactory for CollectListEvaluator {
    fn try_new(_info: StaticInfo<'_>) -> anyhow::Result<Box<dyn Evaluator>> {
        unimplemented!("list collect evaluator is unsupported")
    }
}

impl Evaluator for CollectListEvaluator {
    fn evaluate(&mut self, _info: &dyn RuntimeInfo) -> anyhow::Result<ArrayRef> {
        unimplemented!("list collect evaluator is unsupported")
    }
}
