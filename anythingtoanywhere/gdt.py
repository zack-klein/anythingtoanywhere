from anythingtoanywhere.destinations import SUPPORTED_DESTINATIONS
from anythingtoanywhere.sources import SUPPORTED_SOURCES


class GenericDataTransfer:
    def __init__(self, source, destination, **kwargs):
        self.source = SUPPORTED_SOURCES.get(source)
        self.destination = SUPPORTED_DESTINATIONS.get(destination)

        self._validate(**kwargs)

    def _validate(self, **kwargs):
        self._validate_source_and_destination()

        # Validates and sets reader/writer options
        self.reader_options = self.source.get_reader_options(**kwargs)
        self.writer_options = self.destination.get_writer_options(**kwargs)

        self.reader = self.source.get_reader()
        self.writer = self.destination.get_writer()

    def _validate_source_and_destination(self):
        invalid_options = []
        if not self.source:
            invalid_options.append("source")
        if not self.destination:
            invalid_options.append("destination")

        if len(invalid_options) > 0:
            raise ValueError(
                f"Invalid options provided: {', '.join(invalid_options)}"
            )

    def execute(self):
        reader = self.reader
        reader_options = self.reader_options
        writer = self.writer
        writer_options = self.writer_options

        content = reader(**reader_options)
        writer(content, **writer_options)
