class UnexpectedResult(Exception):
    """The REST API returned a result that violates our assumptions."""


class InvalidPageFormat(Exception):
    """The REST API returned an invalid JSON message."""
    def __init__(self, input):
        super(InvalidPageFormat, self).__init__(
        	'Unexpected input: {!r}'.format(input)
        )
