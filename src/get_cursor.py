from sqlite3 import Connection


def get_cursor(path, get_db=True):
    """
    `return` a `Cursor` object for the sqlite3 database specified by "path",
    which must be a string. Also `return` a `Connection` object by default,
    unless `get_db` is set to `False`.
    """

    db = Connection(path)
    curs = db.cursor()
    if get_db:
        return curs, db
    else:
        return curs