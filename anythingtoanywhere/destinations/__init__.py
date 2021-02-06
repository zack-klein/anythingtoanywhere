from anythingtoanywhere import types
from anythingtoanywhere.destinations.local_filesystem import LocalFilesystem
from anythingtoanywhere.destinations.s3 import S3
from anythingtoanywhere.destinations.dropbox import Dropbox


SUPPORTED_DESTINATIONS = {
    types.LOCAL_FILESYSTEM: LocalFilesystem,
    types.S3: S3,
    types.DROPBOX: Dropbox,
}
