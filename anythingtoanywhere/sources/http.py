import requests

from anythingtoanywhere.sources.base import BaseSource


def request_to_bytes(source_url):
    response = requests.get(source_url)
    return response.content


class HTTP(BaseSource):
    def get_reader():
        return request_to_bytes

    def get_reader_options(**kwargs):
        if "source_url" not in kwargs:
            raise AttributeError(
                f"Required field missing from HTTP reader: source_url!"
            )
        else:
            return {"source_url": kwargs["source_url"]}


class HTTPS(BaseSource):
    def get_reader():
        return request_to_bytes

    def get_reader_options(**kwargs):
        if "source_url" not in kwargs:
            raise AttributeError(
                f"Required field missing from HTTPS reader: source_url!"
            )
        else:
            return {"source_url": kwargs["source_url"]}
