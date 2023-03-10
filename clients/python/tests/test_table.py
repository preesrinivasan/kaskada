import os
from pathlib import Path
from unittest.mock import call, patch

import google.protobuf.wrappers_pb2 as wrappers
import pandas as pd
import pytest

import kaskada.client
import kaskada.kaskada.v1alpha.common_pb2 as common_pb
import kaskada.kaskada.v1alpha.table_service_pb2 as table_pb
import kaskada.table


@patch("kaskada.client.Client")
def test_table_create_table_default_values(mockClient):
    table_name = "test_table"
    time_column_name = "time"
    entity_key_column_name = "entity"
    expected_request = table_pb.CreateTableRequest(
        table=table_pb.Table(
            table_name=table_name,
            time_column_name=time_column_name,
            entity_key_column_name=entity_key_column_name,
        )
    )
    kaskada.table.create_table(
        table_name, time_column_name, entity_key_column_name, client=mockClient
    )
    mockClient.table_stub.CreateTable.assert_called_with(
        expected_request, metadata=mockClient.get_metadata()
    )


@patch("kaskada.client.Client")
def test_table_create_table_grouping_id(mockClient):
    table_name = "test_table"
    time_column_name = "time"
    entity_key_column_name = "entity"
    grouping_id = "my_grouping_id"
    expected_request = table_pb.CreateTableRequest(
        table=table_pb.Table(
            table_name=table_name,
            time_column_name=time_column_name,
            entity_key_column_name=entity_key_column_name,
            grouping_id=grouping_id,
        )
    )
    kaskada.table.create_table(
        table_name,
        time_column_name,
        entity_key_column_name,
        grouping_id=grouping_id,
        client=mockClient,
    )
    mockClient.table_stub.CreateTable.assert_called_with(
        expected_request, metadata=mockClient.get_metadata()
    )


@patch("kaskada.client.Client")
def test_table_create_table_subsort_column_id(mockClient):
    table_name = "test_table"
    time_column_name = "time"
    entity_key_column_name = "entity"
    subsort_column_name = "my_subsort_column"
    expected_request = table_pb.CreateTableRequest(
        table=table_pb.Table(
            table_name=table_name,
            time_column_name=time_column_name,
            entity_key_column_name=entity_key_column_name,
            subsort_column_name=wrappers.StringValue(value=subsort_column_name),
        )
    )
    kaskada.table.create_table(
        table_name,
        time_column_name,
        entity_key_column_name,
        subsort_column_name=subsort_column_name,
        client=mockClient,
    )
    mockClient.table_stub.CreateTable.assert_called_with(
        expected_request, metadata=mockClient.get_metadata()
    )


def test_pulsar_table_source():
    protocol = "pulsar://localhost:6650"
    topic = "my-topic"
    test_source = kaskada.table.PulsarTableSource(protocol, topic)
    assert test_source._protocol_url == protocol
    assert test_source._topic == topic


@patch("kaskada.client.Client")
def test_table_create_table_with_pulsar_table_source(mockClient):
    table_name = "test_table"
    time_column_name = "time"
    entity_key_column_name = "entity"
    protocol_url = "pulsar://localhost:6650"
    topic = "my-topic"
    test_source = kaskada.table.PulsarTableSource(protocol_url, topic)
    expected_request = table_pb.CreateTableRequest(
        table=table_pb.Table(
            table_name=table_name,
            time_column_name=time_column_name,
            entity_key_column_name=entity_key_column_name,
            table_source={
                "pulsar": table_pb.Table.PulsarSource(
                    **{"protocol_url": protocol_url, "topic": topic}
                )
            },
        )
    )
    kaskada.table.create_table(
        table_name,
        time_column_name,
        entity_key_column_name,
        source=test_source,
        client=mockClient,
    )
    mockClient.table_stub.CreateTable.assert_called_with(
        expected_request, metadata=mockClient.get_metadata()
    )


@patch("kaskada.client.Client")
def test_table_create_table_with_invalid_table_source(mockClient):
    table_name = "test_table"
    time_column_name = "time"
    entity_key_column_name = "entity"
    test_source = kaskada.table.TableSource()
    with pytest.raises(Exception):
        kaskada.table.create_table(
            table_name,
            time_column_name,
            entity_key_column_name,
            source=test_source,
            client=mockClient,
        )


@patch("kaskada.client.Client")
def test_table_load_parquet(mockClient):
    table_name = "test_table"
    local_file = "local.parquet"
    expected_request = table_pb.LoadDataRequest(
        table_name=table_name,
        file_input=common_pb.FileInput(
            file_type="FILE_TYPE_PARQUET", uri=f"file://{Path(local_file).absolute()}"
        ),
    )

    kaskada.table.load(table_name, local_file, client=mockClient)
    mockClient.table_stub.LoadData.assert_called_with(
        expected_request, metadata=mockClient.get_metadata()
    )


@patch("kaskada.client.Client")
def test_table_load_csv(mockClient):
    table_name = "test_table"
    local_file = "local.csv"
    expected_request = table_pb.LoadDataRequest(
        table_name=table_name,
        file_input=common_pb.FileInput(
            file_type="FILE_TYPE_CSV", uri=f"file://{Path(local_file).absolute()}"
        ),
    )

    kaskada.table.load(table_name, local_file, client=mockClient)
    mockClient.table_stub.LoadData.assert_called_with(
        expected_request, metadata=mockClient.get_metadata()
    )


@patch("kaskada.client.Client")
def test_table_load_invalid_type(mockClient):
    table_name = "test_table"
    local_file = "local.img"
    with pytest.raises(Exception):
        kaskada.table.load(table_name, local_file, client=mockClient)


@patch("kaskada.client.Client")
def test_table_load_dataframe(mockClient):
    table_name = "test_table"
    transactions_parquet = str(
        Path(__file__).parent.joinpath("transactions.parquet").absolute()
    )
    df = pd.read_parquet(transactions_parquet)
    expected_request = table_pb.LoadDataRequest(
        table_name=table_name,
        file_input=common_pb.FileInput(
            file_type="FILE_TYPE_CSV", uri=f"file://{transactions_parquet}"
        ),
    )
    kaskada.table.load_dataframe(table_name=table_name, dataframe=df, client=mockClient)
    assert mockClient.get_metadata.call_args_list == [call()]
    mockClient.table_stub.LoadData.assert_called_once()
