"""
Exceptions used in all application
"""


class InvalidNetlocException(Exception):
    """Raised when the netloc (host:port) is invalid"""

    def __init__(self):
        super().__init__("The port and/or host is incorrect")
