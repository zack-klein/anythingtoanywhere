from anythingtoanywhere import types
from anythingtoanywhere.sources.local_filesystem import LocalFilesystem
from anythingtoanywhere.sources.s3 import S3
from anythingtoanywhere.sources.dropbox import Dropbox


SUPPORTED_SOURCES = {
    types.LOCAL_FILESYSTEM: LocalFilesystem,
    types.S3: S3,
    types.DROPBOX: Dropbox,
}
