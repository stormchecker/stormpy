class StormError(Exception):
    """
    Base class for exceptions in Storm.
    """

    def __init__(self, message: str):
        """
        Constructor.

        :param message: Error message.
        :type message: str
        """
        self.message = "Storm: " + message
