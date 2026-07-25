from app.exceptions.error_codes import ErrorCode


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        status_code: int,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)


class CompanyNotFoundException(AppException):
    def __init__(self, company: str):
        super().__init__(
            message=f"Company '{company}' not found.",
            error_code=ErrorCode.COMPANY_NOT_FOUND,
            status_code=404,
        )


class NewsNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message="No news found.",
            error_code=ErrorCode.NEWS_NOT_FOUND,
            status_code=404,
        )


class ResearchNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message="Research data not found.",
            error_code=ErrorCode.RESEARCH_NOT_FOUND,
            status_code=404,
        )


class DatabaseException(AppException):
    def __init__(self, message="Database operation failed."):
        super().__init__(
            message=message,
            error_code=ErrorCode.DATABASE_ERROR,
            status_code=500,
        )


class ExternalAPIException(AppException):
    def __init__(self, message="External service unavailable."):
        super().__init__(
            message=message,
            error_code=ErrorCode.EXTERNAL_API_ERROR,
            status_code=502,
        )


class MCPException(AppException):
    def __init__(self, message="MCP request failed."):
        super().__init__(
            message=message,
            error_code=ErrorCode.MCP_ERROR,
            status_code=500,
        )


class LLMServiceException(AppException):
    def __init__(self, message="LLM service unavailable."):
        super().__init__(
            message=message,
            error_code=ErrorCode.LLM_ERROR,
            status_code=503,
        )


class InvalidRequestException(AppException):
    def __init__(self, message="Invalid request."):
        super().__init__(
            message=message,
            error_code=ErrorCode.INVALID_REQUEST,
            status_code=400,
        )