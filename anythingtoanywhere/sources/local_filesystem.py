from anythingtoanywhere.sources.base import BaseSource


def local_file_to_bytes(source_file_path):
    with open(source_file_path, "rb") as f:
        content = f.read()
    return content


class LocalFilesystem(BaseSource):
    def get_reader():
        return local_file_to_bytes

    def get_reader_options(**kwargs):
        if "source_file_path" not in kwargs:
            raise AttributeError(
                f"Required field missing from local reader: source_file_path!"
            )
        else:
            return {"source_file_path": kwargs["source_file_path"]}
