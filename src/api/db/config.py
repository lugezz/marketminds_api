from decouple import Config, RepositoryEnv


# config = Config()
config = Config(repository=RepositoryEnv('../.env.local'))


DATABASE_CONFIG = {
    "user": config("MYSQL_USER", default="root"),
    "password": config("MYSQL_PASSWORD", default=""),
    "host": config("MYSQL_HOST", default="localhost"),
    "port": config("MYSQL_PORT", default="3306"),
    "database": config("MYSQL_DATABASE", default="market_minds_db"),
}

DATABASE_URL = (
    f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)


def get_db_url() -> str:
    """ Get the database URL.
    """
    if not DATABASE_URL:
        raise NotImplementedError("DATABASE_URL is not set")
    return DATABASE_URL
