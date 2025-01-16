from __future__ import annotations
__all__ = ['StormError']
class StormError(Exception):
    """
    
        Base class for exceptions in Storm.
        
    """
    def __init__(self, message):
        """
        
                Constructor.
                :param message: Error message.
                
        """
