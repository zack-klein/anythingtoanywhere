import boto3

from anythingtoanywhere.sources.base import BaseSource
from anythingtoanywhere.utils import parse_s3_uri


def s3_to_bytes(source_s3_uri):
    bucket, key = parse_s3_uri(source_s3_uri)
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket, key)
    content = obj.get()["Body"].read()
    return content


class S3(BaseSource):
    def get_reader():
        return s3_to_bytes

    def get_reader_options(**kwargs):
        if "source_s3_uri" not in kwargs:
            raise AttributeError(
                f"Required field missing from S3 reader: source_s3_uri!"
            )
        else:
            return {"source_s3_uri": kwargs["source_s3_uri"]}
