import logging

from sqlalchemy import create_engine

from anythingtoanywhere import types
from anythingtoanywhere.destinations import SUPPORTED_DESTINATIONS
from anythingtoanywhere.sources import SUPPORTED_SOURCES


class GenericDataTransfer:
    def __init__(self, source, destination, **kwargs):
        self._source = source
        self._destination = destination

        self._validate(**kwargs)

    def _validate(self, **kwargs):
        # Validates and sets the source/destination
        self._validate_source_and_destination(**kwargs)

        # Validates and sets reader/writer options
        self.reader_options = self.source.get_reader_options(**kwargs)
        self.writer_options = self.destination.get_writer_options(**kwargs)

        # Checks no extra parameters were sent
        self._validate_no_extra_kwargs(**kwargs)

        self.reader = self.source.get_reader()
        self.writer = self.destination.get_writer()

    def _is_sqlalchemy(self, uri):
        try:
            create_engine(uri)
            is_sqlalchemy = True
        except Exception as e:
            logging.exception(e)
            is_sqlalchemy = False
        finally:
            return is_sqlalchemy

    def _validate_source_and_destination(self, **kwargs):
        invalid_options = []

        source = SUPPORTED_SOURCES.get(self._source)
        destination = SUPPORTED_DESTINATIONS.get(self._destination)

        if not source:
            if self._is_sqlalchemy(kwargs.get("source_conn_string")):
                self._source = types.SQLALCHEMY
                source = SUPPORTED_SOURCES.get(types.SQLALCHEMY)
            else:
                invalid_options.append(f"source: {self._source}")

        if not destination:
            if self._is_sqlalchemy(kwargs.get("dest_conn_string")):
                self._destination = types.SQLALCHEMY
                destination = SUPPORTED_DESTINATIONS.get(types.SQLALCHEMY)
            else:
                invalid_options.append(f"destination: {self._destination}")

        if len(invalid_options) > 0:
            raise ValueError(
                f"Invalid options provided: {', '.join(invalid_options)}"
            )
        else:
            self.source = source
            self.destination = destination

    def _validate_no_extra_kwargs(self, **kwargs):
        extra_kwargs = []
        for kwarg in kwargs:
            if (
                kwarg not in self.reader_options
                and kwarg not in self.writer_options
            ):
                extra_kwargs.append(kwarg)

        if len(extra_kwargs) > 0:
            raise ValueError(
                f"Unrecognized arguments passed: {', '.join(extra_kwargs)}"
            )

    def execute(self):
        reader = self.reader
        reader_options = self.reader_options
        writer = self.writer
        writer_options = self.writer_options

        content = reader(**reader_options)
        writer(content, **writer_options)
