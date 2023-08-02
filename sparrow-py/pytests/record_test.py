"""Tests for the Kaskada query builder."""
import pytest
import sparrow_py as s
from sparrow_py.sources import CsvSource


@pytest.fixture
def source() -> CsvSource:
    """Create an empty table for testing."""
    content = "\n".join(
        [
            "time,key,m,n",
            "1996-12-19T16:39:57-08:00,A,5,10",
            "1996-12-19T16:39:58-08:00,B,24,3",
            "1996-12-19T16:39:59-08:00,A,17,6",
            "1996-12-19T16:40:00-08:00,A,,9",
            "1996-12-19T16:40:01-08:00,A,12,",
            "1996-12-19T16:40:02-08:00,A,,",
        ]
    )
    return CsvSource("time", "key", content)


def test_record(source) -> None:
    """Test we can create a record."""
    m = source["m"]
    n = source["n"]
    result = s.record(
        {
            "m": m,
            "n": n,
        }
    ).run_to_csv_string()

    assert result == "\n".join(
        [
            "_time,_subsort,_key_hash,_key,m,n",
            "1996-12-20 00:39:57,0,12960666915911099378,A,5.0,10.0",
            "1996-12-20 00:39:58,1,2867199309159137213,B,24.0,3.0",
            "1996-12-20 00:39:59,2,12960666915911099378,A,17.0,6.0",
            "1996-12-20 00:40:00,3,12960666915911099378,A,,9.0",
            "1996-12-20 00:40:01,4,12960666915911099378,A,12.0,",
            "1996-12-20 00:40:02,5,12960666915911099378,A,,",
            "",
        ]
    )


def test_extend_record(source) -> None:
    """Test we can create a record."""
    m = source["m"]
    n = source["n"]
    result = source.extend({"add": m + n}).run_to_csv_string()
    print(result)

    assert result == "\n".join(
        [
            "_time,_subsort,_key_hash,_key,add,time,key,m,n",
            "1996-12-20 00:39:57,0,12960666915911099378,A,15.0,1996-12-19T16:39:57-08:00,A,5.0,10.0",
            "1996-12-20 00:39:58,1,2867199309159137213,B,27.0,1996-12-19T16:39:58-08:00,B,24.0,3.0",
            "1996-12-20 00:39:59,2,12960666915911099378,A,23.0,1996-12-19T16:39:59-08:00,A,17.0,6.0",
            "1996-12-20 00:40:00,3,12960666915911099378,A,,1996-12-19T16:40:00-08:00,A,,9.0",
            "1996-12-20 00:40:01,4,12960666915911099378,A,,1996-12-19T16:40:01-08:00,A,12.0,",
            "1996-12-20 00:40:02,5,12960666915911099378,A,,1996-12-19T16:40:02-08:00,A,,",
            "",
        ]
    )


def test_select_record(source) -> None:
    """Test we can select some fields from a record."""
    result = source.select("m", "n").run_to_csv_string()
    print(result)
    assert result == "\n".join(
        [
            "_time,_subsort,_key_hash,_key,time,key,m",
            "1996-12-20 00:39:57,0,12960666915911099378,A,1996-12-19T16:39:57-08:00,A,5.0",
            "1996-12-20 00:39:58,1,2867199309159137213,B,1996-12-19T16:39:58-08:00,B,24.0",
            "1996-12-20 00:39:59,2,12960666915911099378,A,1996-12-19T16:39:59-08:00,A,17.0",
            "1996-12-20 00:40:00,3,12960666915911099378,A,1996-12-19T16:40:00-08:00,A,",
            "1996-12-20 00:40:01,4,12960666915911099378,A,1996-12-19T16:40:01-08:00,A,12.0",
            "1996-12-20 00:40:02,5,12960666915911099378,A,1996-12-19T16:40:02-08:00,A,",
            "",
        ]
    )
