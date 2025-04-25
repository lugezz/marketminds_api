import logging
from sqlmodel import Session, create_engine, SQLModel

from api.db.config import get_db_url


logger = logging.getLogger(__name__)

data_base_url = get_db_url()

# Ensure the database URL is correct
if not data_base_url:
    raise ValueError("Database URL is not configured properly.")

engine = create_engine(data_base_url, echo=True)


def init_db():
    """ Initialize the database.
    """
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        logger.error(f"Failed to initialize the database: {e}")
        raise
    logger.info("Initializing the database...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database initialized.")


def get_session() -> Session:
    """ Get a new database session.
    """
    logger.debug("Creating a new database session...")
    with Session(engine) as session:
        yield session
        logger.debug("Database session closed.")
