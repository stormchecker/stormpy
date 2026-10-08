class StormWarning(Warning):
    """
    Base class for warnings in Storm.
    """

    def __init__(self, message: str):
        """
        Constructor.

        :param message: Warning message.
        :type message: str
        """
        self.message = "Storm warning: " + message
        super().__init__(self.message)
