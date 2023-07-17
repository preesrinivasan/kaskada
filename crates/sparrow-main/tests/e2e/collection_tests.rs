//! e2e tests for the collection operators.

use sparrow_api::kaskada::v1alpha::TableConfig;
use uuid::Uuid;

use crate::{fixture::DataFixture, QueryFixture};

/// Create a simple table with a collection type (map).
///
/// ```json
/// {"time": 2000, "key": 1, "e0": {"f1": 0,  "f2": 22}, "e1": 1,  "e2": 2.7,  "e3": "f1" }
/// {"time": 3000, "key": 1, "e0": {"f1": 1,  "f2": 10}, "e1": 2,  "e2": 3.8,  "e3": "f2" }
/// {"time": 3000, "key": 1, "e0": {"f1": 5,  "f2": 3},  "e1": 42, "e2": 4.0,  "e3": "f3" }
/// {"time": 3000, "key": 1, "e0": {"f2": 13},           "e1": 42, "e2": null, "e3": "f2" }
/// {"time": 4000, "key": 1, "e0": {"f1": 15, "f3": 11}, "e1": 3,  "e2": 7,    "e3": "f3" }
/// ```
pub(crate) async fn collection_data_fixture() -> DataFixture {
    DataFixture::new()
        .with_table_from_files(
            TableConfig::new_with_table_source("Input", &Uuid::new_v4(), "time", None, "key", ""),
            &[&"parquet/data_with_map.parquet"],
        )
        .await
        .unwrap()
}

pub(crate) async fn supplant_data_fixture() -> DataFixture {
    DataFixture::new()
        .with_table_from_files(
            TableConfig::new_with_table_source(
                "Input",
                &Uuid::new_v4(),
                "timestamp_utc",
                None,
                "system_serial",
                "",
            ),
            &[&"parquet/supplant.parquet"],
        )
        .await
        .unwrap()
}

#[tokio::test]
async fn test_get_static_key() {
    insta::assert_snapshot!(QueryFixture::new("{ f1: get(\"f1\", Input.e0) }").run_to_csv(&collection_data_fixture().await).await.unwrap(), @r###"
    _time,_subsort,_key_hash,_key,f1
    1970-01-01T00:00:00.000002000,5039430902799166705,2359047937476779835,1,0
    1970-01-01T00:00:00.000003000,5039430902799166706,2359047937476779835,1,1
    1970-01-01T00:00:00.000003000,5039430902799166707,2359047937476779835,1,5
    1970-01-01T00:00:00.000003000,5039430902799166708,2359047937476779835,1,
    1970-01-01T00:00:00.000004000,5039430902799166709,2359047937476779835,1,15
    "###);
}

#[tokio::test]
async fn test_get_static_key_second_field() {
    insta::assert_snapshot!(QueryFixture::new("{ f2: Input.e0 | get(\"f2\") }").run_to_csv(&collection_data_fixture().await).await.unwrap(), @r###"
    _time,_subsort,_key_hash,_key,f2
    1970-01-01T00:00:00.000002000,5039430902799166705,2359047937476779835,1,22
    1970-01-01T00:00:00.000003000,5039430902799166706,2359047937476779835,1,10
    1970-01-01T00:00:00.000003000,5039430902799166707,2359047937476779835,1,3
    1970-01-01T00:00:00.000003000,5039430902799166708,2359047937476779835,1,13
    1970-01-01T00:00:00.000004000,5039430902799166709,2359047937476779835,1,
    "###);
}

#[tokio::test]
async fn test_get_dynamic_key() {
    insta::assert_snapshot!(QueryFixture::new("{ value: Input.e0 | get(Input.e3) }").run_to_csv(&collection_data_fixture().await).await.unwrap(), @r###"
    _time,_subsort,_key_hash,_key,value
    1970-01-01T00:00:00.000002000,5039430902799166705,2359047937476779835,1,0
    1970-01-01T00:00:00.000003000,5039430902799166706,2359047937476779835,1,10
    1970-01-01T00:00:00.000003000,5039430902799166707,2359047937476779835,1,
    1970-01-01T00:00:00.000003000,5039430902799166708,2359047937476779835,1,13
    1970-01-01T00:00:00.000004000,5039430902799166709,2359047937476779835,1,11
    "###);
}

#[tokio::test]
async fn test_supplant() {
    insta::assert_snapshot!(QueryFixture::new("{ value: get(\"airTemperature\", Input.readings) | when(is_valid($input)) } ").with_dump_dot("asdf").run_to_csv(&supplant_data_fixture().await).await.unwrap(), @r###"
    _time,_subsort,_key_hash,_key,value
    "###);
}

#[tokio::test]
async fn test_swapped_args_for_get_map() {
    insta::assert_yaml_snapshot!(QueryFixture::new("{ f1: get(Input.e0, \"f1\") }")
        .run_to_csv(&collection_data_fixture().await).await.unwrap_err(), @r###"
    ---
    code: Client specified an invalid argument
    message: 1 errors in Fenl statements; see diagnostics
    fenl_diagnostics:
      - severity: error
        code: E0010
        message: Invalid argument type(s)
        formatted:
          - "error[E0010]: Invalid argument type(s)"
          - "  --> Query:1:7"
          - "  |"
          - "1 | { f1: get(Input.e0, \"f1\") }"
          - "  |       ^^^           ---- Actual type: string"
          - "  |       |              "
          - "  |       Invalid types for parameter 'map' in call to 'get'"
          - "  |"
          - "  --> built-in signature 'get<K: key, V: any>(key: K, map: map<K, V>) -> V':1:34"
          - "  |"
          - "1 | get<K: key, V: any>(key: K, map: map<K, V>) -> V"
          - "  |                                  --------- Expected type: map<K, V>"
          - ""
          - ""
    "###);
}
