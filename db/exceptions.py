class DBIntegrityError(Exception):
    pass


class DBDataError(Exception):
    pass


class DBLoginExistsException(Exception):
    pass


class DBLoginDoesntExistException(Exception):
    pass


