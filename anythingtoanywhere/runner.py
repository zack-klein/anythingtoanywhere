from anythingtoanywhere import types
from anythingtoanywhere.gdt import GenericDataTransfer

from urllib.parse import urlparse


def infer_location(path):
    parsed = urlparse(path)
    if not parsed.scheme:
        source = types.LOCAL_FILESYSTEM
    else:
        source = parsed.scheme
    return source


def guess_source_kwargs(source, path):
    if source == types.S3:
        return {"source_s3_uri": path}
    elif source == types.DROPBOX:
        return {"source_dropbox_uri": path}
    elif source == types.HTTP or source == types.HTTPS:
        return {"source_url": path}
    elif source == types.LOCAL_FILESYSTEM:
        return {"source_file_path": path}
    else:  # We assume it's sqlalchemy since there are a bunch of options!
        return {"dest_conn_string": path}


def guess_destination_kwargs(source, path):
    if source == types.S3:
        return {"dest_s3_uri": path}
    elif source == types.DROPBOX:
        return {"dest_dropbox_uri": path}
    elif source == types.LOCAL_FILESYSTEM:
        return {"dest_file_path": path}
    else:  # We assume it's sqlalchemy since there are a bunch of options!
        return {"dest_conn_string": path}


def copy(source, destination, **kwargs):

    # Pull out location
    from_where = infer_location(source)
    to_where = infer_location(destination)

    # See if we can infer any kwargs
    from_options = guess_source_kwargs(from_where, source)
    to_options = guess_destination_kwargs(to_where, destination)
    kwargs.update(from_options)
    kwargs.update(to_options)

    # Run the transfer!
    transfer_operation = GenericDataTransfer(from_where, to_where, **kwargs)
    transfer_operation.execute()

    # Return some metadata
    return {
        "source": transfer_operation._source,
        "destination": transfer_operation._destination,
    }
