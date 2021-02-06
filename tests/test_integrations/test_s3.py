import os
import tempfile
import uuid

import boto3

from anythingtoanywhere import copy
from anythingtoanywhere.destinations.s3 import bytes_to_s3
from anythingtoanywhere.utils import parse_s3_uri

from tests.constant import RUN_ID, FAKE

BUCKET = os.getenv("TEST_S3_BUCKET")

S3_URI_PREFIX = f"s3://{BUCKET}/anythingtoanywhere-unittests/{RUN_ID}"


def random_s3_key():
    rand = str(uuid.uuid4())
    path = f"{S3_URI_PREFIX}/{rand}"
    return path


def random_s3_file():
    expected_content = bytes(FAKE.bs(), "utf-8")
    path = random_s3_key()
    bytes_to_s3(expected_content, path)
    return path, expected_content


def get_s3_obj(uri):
    bucket, key = parse_s3_uri(uri)
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket, key)
    return obj


def get_s3_obj_content(uri):
    obj = get_s3_obj(uri)
    return obj.get()["Body"].read()


def delete_s3_obj(uri):
    obj = get_s3_obj(uri)
    obj.delete()


def test_local_to_s3():

    expected_content = b"Just trying to keep the customer satisfied!"

    with tempfile.TemporaryDirectory() as tmp:
        sourcename = tmp + "TEMPORARYSOURCE"
        destname = f"{S3_URI_PREFIX}/{sourcename}"

        with open(sourcename, "wb") as f:
            f.write(expected_content)
            f.seek(0)

        copy(sourcename, destname)
        actual_content = get_s3_obj_content(destname)

        assert actual_content == expected_content
        delete_s3_obj(destname)


def test_s3_to_local():
    sourcename, expected_content = random_s3_file()

    with tempfile.TemporaryDirectory() as tmp:
        destname = tmp + "foo"
        copy(sourcename, destname)

        with open(destname, "rb") as f:
            actual_content = f.read()

    assert actual_content == expected_content

    delete_s3_obj(sourcename)


def test_s3_to_s3():

    sourcename, expected_content = random_s3_file()
    destname = random_s3_key()

    copy(sourcename, destname)

    actual_content = get_s3_obj_content(destname)

    assert actual_content == expected_content

    delete_s3_obj(sourcename)
    delete_s3_obj(destname)


def test_dropbox_to_s3():
    pass
