from decouple import config


DATABASE_URL = config("DATABASE_URL", default="sqlite:///./test.db")


def get_db_url() -> str:
    """ Get the database URL.
    """
    if not DATABASE_URL:
        raise NotImplementedError("DATABASE_URL is not set")
    return DATABASE_URL
