import pytest

import sparrow_py as kt


@pytest.fixture(scope="module")
def source() -> kt.sources.CsvString:
    content = "\n".join(
        [
            "time,key,m,n,str",
            '1996-12-19T16:39:57,A,5,10,"apple"',
            '1996-12-19T16:39:58,B,24,3,"dog"',
            '1996-12-19T16:39:59,A,17,6,"carrot"',
            "1996-12-19T16:40:00,A,,9,",
            '1996-12-19T16:40:01,A,12,,"eggplant"',
            '1996-12-19T16:40:02,A,,,"fig"',
        ]
    )
    return kt.sources.CsvString(content, time_column_name="time", key_column_name="key")


def test_length(source, golden) -> None:
    my_str = source.col("str")
    list = my_str.collect(max=None)
    golden.jsonl(
        kt.record(
            {
                "str": my_str,
                "len_key": my_str.length(),
                "list": list,
                "len_list": list.length(),
            }
        )
    )
