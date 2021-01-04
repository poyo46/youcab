class YoucabError(Exception):
    """
    Base class for exceptions in this module.
    """

    pass


class NotFoundNodeFormatError(YoucabError):
    """
    Raised when the ``node-format`` could not be set automatically.
    """

    pass


class InvalidTokenizerError(YoucabError):
    """
    Raised when the tokenizer is not working properly.
    """

    pass


class MecabConfigError(YoucabError):
    """
    Raised when the ``mecab-config`` command is not found.
    """

    pass
