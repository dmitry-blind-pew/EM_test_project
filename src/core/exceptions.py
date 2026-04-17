from fastapi import HTTPException


class EMPException(HTTPException):
    status_code = 500
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.status_code, self.detail, *args, **kwargs)


class BadRequestException(EMPException):
    status_code = 400
    detail = "Passwords do not match"


class UnauthorizedException(EMPException):
    status_code = 401
    detail = "Unauthorized"


class ForbiddenException(EMPException):
    status_code = 403
    detail = "Forbidden"


class DataNotFoundException(EMPException):
    status_code = 404
    detail = "Data not found"


class UserNotFoundException(EMPException):
    status_code = 404
    detail = "User not found"


class UserAlreadyExistsException(EMPException):
    status_code = 400
    detail = "User already exists"
