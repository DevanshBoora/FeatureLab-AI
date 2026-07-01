class FeatureLabException(Exception):
    """Base exception for all FeatureLab exceptions"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class DomainException(FeatureLabException):
    """Raised when a domain rule is violated"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)

class ValidationException(FeatureLabException):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=422)

class ResourceNotFoundException(FeatureLabException):
    """Raised when a resource is not found"""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)

class PipelineException(FeatureLabException):
    """Raised when a pipeline execution fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)

class StorageException(FeatureLabException):
    """Raised when a storage operation fails"""
    def __init__(self, message: str):
        super().__init__(message, status_code=502)
