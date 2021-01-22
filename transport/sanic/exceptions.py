from sanic.exceptions import SanicException


class SanicRequestValidationException(SanicException):
    status_code = 400


class SanicUserConflictException(SanicException):
    status_code = 409


class SanicDBException(SanicException):
    status_code = 500


class SanicResponceValidationException(SanicException):
    status_code = 500


class SanicPasswordHashException(SanicException):
    status_code = 400


class SanicDBException(SanicException):
    status_code = 500


class SanicLoginExistsException(SanicException):
    status_code = 400


class SanicDBLoginNotFound(SanicException):
    status_code = 404


class SanicTokenIsNotReadable(SanicException):
    status_code = 401


class SanicUserNotFound(SanicException):
    status_code = 404


class SanicUserNotExists(SanicException):
    status_code = 400


class SanicMessageNotFound(SanicException):
    status_code = 404
