class APIRequestException(Exception):
    """Exception levée pour les erreurs de requêtes API."""
    def __init__(self, message):
        super().__init__(message)

class APITimeoutException(APIRequestException):
    """Exception levée lorsqu'une requête API expire."""
    pass

class APIHTTPErrorException(APIRequestException):
    """Exception levée lorsqu'une erreur HTTP survient."""
    pass

class GeneralAPIException(APIRequestException):
    """Exception levée pour les autres erreurs API."""
    pass
    