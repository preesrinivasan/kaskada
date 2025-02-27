import pytest

import sparrow_py as kt


@pytest.fixture(scope="module")
def source() -> kt.sources.CsvString:
    content = "\n".join(
        [
            "time,key,m,n",
            "1996-12-19T16:39:57,A,5,10",
            "1996-12-19T16:39:58,B,24,3",
            "1996-12-19T16:39:59,A,17,6",
            "1996-12-19T16:40:00,A,,9",
            "1996-12-19T16:40:01,A,12,",
            "1996-12-19T16:40:02,A,,",
        ]
    )
    return kt.sources.CsvString(content, time_column_name="time", key_column_name="key")


def test_lag(source, golden) -> None:
    m = source.col("m")
    n = source.col("n")
    golden.jsonl(
        kt.record(
            {
                "m": m,
                "lag_1_m": m.lag(1),
                "lag_2_m": m.lag(2),
                "n": n,
                "lag_1_n": n.lag(1),
                "lag_2_n": n.lag(2),
            }
        )
    )


def test_lag_struct(source, golden) -> None:
    golden.jsonl(source.lag(1))


def test_lag_list(source, golden) -> None:
    m = source.col("m")
    golden.jsonl(
        kt.record(
            {
                "m": m,
                "list_m": m.collect(max=None),
                "lag_list_m": m.collect(max=None).lag(1),
            }
        )
    )
