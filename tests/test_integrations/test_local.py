import tempfile

from anythingtoanywhere import copy

from tests.constant import FAKE


def test_local_to_local():

    expected_content = FAKE.bs()

    with tempfile.TemporaryDirectory() as tmp:
        sourcename = tmp + "TEMPORARYSOURCE"
        destname = tmp + "TEMPORARYDESTINATION"

        with open(sourcename, "w") as f:
            f.write(expected_content)
            f.seek(0)

        copy(sourcename, destname)

        with open(destname) as f:
            actual_content = f.read()

        assert actual_content == expected_content
