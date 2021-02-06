import boto3

from anythingtoanywhere.destinations.base import BaseDestination
from anythingtoanywhere.utils import parse_s3_uri


def bytes_to_s3(content_in_bytes, dest_s3_uri):
    bucket, key = parse_s3_uri(dest_s3_uri)
    s3 = boto3.resource("s3")
    obj = s3.Object(bucket, key)
    obj.put(Body=content_in_bytes)


class S3(BaseDestination):
    def get_writer():
        return bytes_to_s3

    def get_writer_options(**kwargs):
        if "dest_s3_uri" not in kwargs:
            raise AttributeError(
                f"Required field missing from S3 writer: dest_s3_uri!"
            )
        else:
            return {"dest_s3_uri": kwargs["dest_s3_uri"]}
