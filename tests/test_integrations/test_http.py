import tempfile

import requests

from anythingtoanywhere import copy

from tests.test_integrations.test_s3 import random_s3_key, get_s3_obj_content
from tests.test_integrations.test_dropbox import (
    random_dropbox_path,
    get_random_dropbox_file_content,
    DROPBOX_ACCESS_TOKEN,
    clean_dropbox,
)


def test_http_to_local():
    url = "http://zacharyjklein.com"

    with tempfile.TemporaryDirectory() as tmp:
        path = tmp + "/website.html"
        copy(url, path)

        with open(path, "rb") as f:
            actual_content = f.read()

    expected_content = requests.get(url).content

    assert actual_content == expected_content


def test_https_to_local():
    url = "https://zacharyjklein.com"

    with tempfile.TemporaryDirectory() as tmp:
        path = tmp + "/website.html"
        copy(url, path)

        with open(path, "rb") as f:
            actual_content = f.read()

    expected_content = requests.get(url).content

    assert actual_content == expected_content


def test_https_to_s3():
    url = (
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
        "archived_data/archived_daily_case_updates/01-21-2020_2200.csv"
    )
    destination_uri = random_s3_key()
    copy(url, destination_uri)
    expected_content = requests.get(url).content
    actual_content = get_s3_obj_content(destination_uri)
    assert actual_content == expected_content


def test_https_to_dropbox():
    url = (
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/"
        "archived_data/archived_daily_case_updates/01-21-2020_2200.csv"
    )
    destination_uri = random_dropbox_path()
    copy(url, destination_uri, dropbox_access_token=DROPBOX_ACCESS_TOKEN)
    expected_content = requests.get(url).content
    actual_content = get_random_dropbox_file_content(destination_uri)
    assert actual_content == expected_content
    clean_dropbox()
