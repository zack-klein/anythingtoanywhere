from urllib.parse import urlparse


def parse_s3_uri(uri):
    """
    https://stackoverflow.com/questions/42641315/s3-urls-get-bucket-name-and-path
    """
    o = urlparse(uri)
    bucket = o.netloc
    key = o.path.lstrip("/")
    return bucket, key
