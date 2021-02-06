from dropbox import Dropbox as DropboxClient

from anythingtoanywhere.sources.base import BaseSource


def dropbox_to_bytes(source_dropbox_uri, dropbox_access_token):
    path = source_dropbox_uri.replace("dropbox://", "")
    dbx = DropboxClient(dropbox_access_token)
    _, response = dbx.files_download(path)
    return response.content


class Dropbox(BaseSource):
    def get_reader():
        return dropbox_to_bytes

    def get_reader_options(**kwargs):
        required_fields = ["source_dropbox_uri", "dropbox_access_token"]
        missing_fields = []
        options = {}

        for field in required_fields:
            if field not in kwargs:
                missing_fields.append(field)
            else:
                options[field] = kwargs[field]

        if len(missing_fields) > 0:
            raise AttributeError(
                f"Required fields missing from Dropbox reader: "
                f"{', '.join(missing_fields)}"
            )
        else:
            return options
