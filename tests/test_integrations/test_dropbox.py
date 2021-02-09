import os
import random
import tempfile
import string

from dropbox import Dropbox

from anythingtoanywhere import copy
from anythingtoanywhere.destinations.dropbox import bytes_to_dropbox
from anythingtoanywhere.sources.dropbox import dropbox_to_bytes

from tests.constant import RUN_ID, FAKE
from tests.test_integrations.test_s3 import (
    random_s3_file,
    get_s3_obj_content,
    delete_s3_obj,
    random_s3_key,
)

DROPBOX_PATH_PREFIX = f"dropbox:///anythingtoanywheretesting/{RUN_ID}"
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")


def clean_dropbox():
    dbx = Dropbox(DROPBOX_ACCESS_TOKEN)
    dbx.files_delete(DROPBOX_PATH_PREFIX.replace("dropbox://", ""))


def random_dropbox_path():
    rand = "".join(random.choice(string.ascii_lowercase) for i in range(10))
    path = f"{DROPBOX_PATH_PREFIX}/{rand}.txt"
    return path


def random_dropbox_file():
    expected_content = bytes(
        FAKE.csv(data_columns=("{{name}}", "{{ipv4}}")), "utf-8"
    )
    path = random_dropbox_path()
    bytes_to_dropbox(expected_content, path, DROPBOX_ACCESS_TOKEN)
    return path, expected_content


def get_random_dropbox_file_content(path):
    return dropbox_to_bytes(
        path.replace("dropbox://", ""), DROPBOX_ACCESS_TOKEN
    )


def test_local_to_dropbox():

    expected_content = b"Somebody once told me the world was gonna rock me"

    with tempfile.TemporaryDirectory() as tmp:
        sourcename = tmp + "TEMPORARYSOURCE"

        with open(sourcename, "wb") as f:
            f.write(expected_content)
            f.seek(0)

        destname = random_dropbox_path()
        copy(sourcename, destname, dropbox_access_token=DROPBOX_ACCESS_TOKEN)
        actual_content = get_random_dropbox_file_content(destname)
        assert actual_content == expected_content
        clean_dropbox()


def test_dropbox_to_local():
    sourcename, expected_content = random_dropbox_file()

    with tempfile.TemporaryDirectory() as tmp:
        destname = tmp + "TEMPORARYDEST"
        copy(sourcename, destname, dropbox_access_token=DROPBOX_ACCESS_TOKEN)

        with open(destname, "rb") as f:
            actual_content = f.read()

    assert actual_content == expected_content
    clean_dropbox()


def test_dropbox_to_dropbox():
    sourcename, expected_content = random_dropbox_file()
    destname = random_dropbox_path()
    copy(sourcename, destname, dropbox_access_token=DROPBOX_ACCESS_TOKEN)
    actual_content = get_random_dropbox_file_content(destname)
    assert expected_content == actual_content
    clean_dropbox()


def test_s3_to_dropbox():
    sourcename, expected_content = random_s3_file()
    destname = random_dropbox_path()
    copy(sourcename, destname, dropbox_access_token=DROPBOX_ACCESS_TOKEN)
    actual_content = get_random_dropbox_file_content(destname)
    assert expected_content == actual_content
    clean_dropbox()
    delete_s3_obj(sourcename)


def test_dropbox_to_s3():
    sourcename, expected_content = random_dropbox_file()
    destname = random_s3_key()
    copy(sourcename, destname, dropbox_access_token=DROPBOX_ACCESS_TOKEN)
    actual_content = get_s3_obj_content(destname)
    assert actual_content == expected_content
    clean_dropbox()
    delete_s3_obj(destname)
