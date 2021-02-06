from dropbox import Dropbox as DropboxClient

from anythingtoanywhere.destinations.base import BaseDestination


def bytes_to_dropbox(content_in_bytes, dest_dropbox_uri, dropbox_access_token):
    path = dest_dropbox_uri.replace("dropbox://", "")
    dbx = DropboxClient(dropbox_access_token)
    dbx.files_upload(
        content_in_bytes, path,
    )


class Dropbox(BaseDestination):
    def get_writer():
        return bytes_to_dropbox

    def get_writer_options(**kwargs):
        required_fields = ["dest_dropbox_uri", "dropbox_access_token"]
        missing_fields = []
        options = {}

        for field in required_fields:
            if field not in kwargs:
                missing_fields.append(field)
            else:
                options[field] = kwargs[field]

        if len(missing_fields) > 0:
            raise AttributeError(
                f"Required fields missing from Dropbox writer: "
                f"{', '.join(missing_fields)}"
            )
        else:
            return options
