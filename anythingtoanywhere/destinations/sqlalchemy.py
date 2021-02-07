from io import BytesIO

import pandas as pd

from sqlalchemy import create_engine

from anythingtoanywhere.destinations.base import BaseDestination


def validate_csv(bytes):
    pass


def bytes_to_sqlalchemy(
    content_in_bytes,
    dest_conn_string,
    dest_table_name,
    dest_schema=None,
    dest_if_exists="fail",
    dest_index=True,
    dest_index_label=None,
    dest_chunksize=None,
    dest_dtype=None,
    dest_method=None,
):
    validate_csv(content_in_bytes)
    df = pd.read_csv(BytesIO(content_in_bytes))
    con = create_engine(dest_conn_string)
    df.to_sql(
        dest_table_name,
        con,
        schema=dest_schema,
        if_exists=dest_if_exists,
        index=dest_index,
        index_label=dest_index_label,
        chunksize=dest_chunksize,
        dtype=dest_dtype,
        method=dest_method,
    )


class SqlAlchemy(BaseDestination):
    def get_writer():
        return bytes_to_sqlalchemy

    def get_writer_options(**kwargs):
        required_fields = ["dest_conn_string", "dest_table_name"]
        optional_fields = [
            "dest_schema",
            "dest_if_exists",
            "dest_index",
            "dest_index_label",
            "dest_chunksize",
            "dest_dtype",
            "dest_method",
        ]
        missing_fields = []
        options = {}

        for field in required_fields:
            if field not in kwargs:
                missing_fields.append(field)
            else:
                options[field] = kwargs[field]

        for field in optional_fields:
            if field in kwargs:
                options[field] = kwargs[field]

        if len(missing_fields) > 0:
            raise AttributeError(
                "Required fields missing from SqlAlchemy writer: "
                f"{', '.join(missing_fields)}!"
            )
        else:
            return options
