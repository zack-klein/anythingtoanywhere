from anythingtoanywhere.destinations.base import BaseDestination


def bytes_to_local(content_in_bytes, dest_file_path):
    with open(dest_file_path, "wb") as f:
        f.write(content_in_bytes)
        f.seek(0)


class LocalFilesystem(BaseDestination):
    def get_writer():
        return bytes_to_local

    def get_writer_options(**kwargs):
        if "dest_file_path" not in kwargs:
            raise AttributeError(
                f"Required field missing from local writer: dest_file_path!"
            )
        else:
            return {"dest_file_path": kwargs["dest_file_path"]}
