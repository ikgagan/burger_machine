# DO NOT EDIT

class OutOfStockException(Exception):
    """Raised when something is out of stock"""
    pass

class NeedsCleaningException(Exception):
    """Raised when the icecream machine needs cleaning"""
    pass

class InvalidChoiceException(Exception):
    """Raised when an invalid choice is picked"""
    pass

class ExceededRemainingChoicesException(Exception):
    """Raised when there are too many scoops of icecream"""
    pass

class InvalidPaymentException(Exception):
    """Raised when an invalid payment amount is given"""
    pass

class InvalidStageException(Exception):
    """Raised when an action occurs in the wrong stage"""
    pass

class NoItemChosenException(Exception):
    """Raised when atleast one topping or scoop isn't picked"""
    pass

class InvalidCombinationException(Exception):
    """Raised when a topping or scoop is picked before a container"""
    pass