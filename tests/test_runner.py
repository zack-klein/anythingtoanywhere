import tempfile

from anythingtoanywhere import copy, types
from tests.constant import FAKE, RUN_ID


def test_local_copy_returns_source_and_dest():

    with tempfile.TemporaryDirectory() as tmp:
        source = tmp + RUN_ID + "source"
        with open(source, "w") as f:
            f.write(FAKE.bs())

        dest = tmp + RUN_ID + "dest"

        results = copy(source, dest)

    assert results == {
        "source": types.LOCAL_FILESYSTEM,
        "destination": types.LOCAL_FILESYSTEM,
    }
