import os
import tempfile

import requests
from sqlalchemy import create_engine

from anythingtoanywhere import copy

from tests.constant import RUN_ID, FAKE
from tests.test_integrations.test_s3 import (
    random_s3_file,
    delete_s3_obj,
)
from tests.test_integrations.test_dropbox import (
    random_dropbox_file,
    clean_dropbox,
    DROPBOX_ACCESS_TOKEN,
)


SQLITE_FILE_PATH = os.getcwd()
CONN_STRING = "sqlite:///anythingtoanywhere.db"


def random_table_name():
    return f"{RUN_ID}_{FAKE.word()}_{FAKE.random_int()}".replace("-", "_")


def get_row_count(table):
    engine = create_engine(CONN_STRING)
    with engine.connect() as connection:
        result = connection.execute(f"select count(*) from '{table}'")
        for row in result:
            count = row[0]

    return count


def drop_table(table):
    engine = create_engine(CONN_STRING)
    with engine.connect() as connection:
        connection.execute(f"drop table '{table}'")


def test_crap_uri_raises():
    conn = "foo:///something.db"
    url = "https://google.com/"
    table_name = random_table_name()
    raised = False
    try:
        copy(url, conn, dest_table_name=table_name)
    except ValueError:
        raised = True

    assert raised


def test_https_to_sqlalchmy():
    url = (
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
        "archived_data/archived_daily_case_updates/01-21-2020_2200.csv"
    )
    table_name = random_table_name()
    copy(url, CONN_STRING, dest_table_name=table_name)
    response = requests.get(url)
    expected_count = response.text.count("\n")
    actual_count = get_row_count(table_name)
    assert actual_count == expected_count
    drop_table(table_name)


def test_local_to_sqlalchemy():
    table_name = random_table_name()
    with tempfile.TemporaryDirectory() as tmp:
        filename = tmp + RUN_ID
        with open(filename, "w") as f:
            content = FAKE.csv(data_columns=("{{name}}", "{{ipv4}}"))
            f.write(content)
            f.seek(0)
        copy(filename, CONN_STRING, dest_table_name=table_name)
    actual_count = get_row_count(table_name)
    assert actual_count == (content.count("\n") - 1)
    drop_table(table_name)


def test_s3_to_sqlalchemy():
    table_name = random_table_name()
    source_path, expected_content = random_s3_file()
    copy(source_path, CONN_STRING, dest_table_name=table_name)
    expected_count = expected_content.decode("utf-8").count("\n") - 1
    actual_count = get_row_count(table_name)
    assert actual_count == expected_count
    drop_table(table_name)
    delete_s3_obj(source_path)


def test_dropbox_to_sqlalchemy():
    table_name = random_table_name()
    source_path, expected_content = random_dropbox_file()
    copy(
        source_path,
        CONN_STRING,
        dest_table_name=table_name,
        dropbox_access_token=DROPBOX_ACCESS_TOKEN,
    )
    expected_count = expected_content.decode("utf-8").count("\n") - 1
    actual_count = get_row_count(table_name)
    assert actual_count == expected_count
    drop_table(table_name)
    clean_dropbox()
