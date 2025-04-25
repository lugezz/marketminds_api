from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.db.session import init_db
from api.marketminds.routing import router as marketmind_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Application lifespan context manager.
    """
    # Before the application starts
    init_db()
    yield
    # Cleanup code can be added here if needed
    # Example: await database.disconnect()


app = FastAPI(title="Event API", lifespan=lifespan)
app.include_router(marketmind_router, prefix="/api/marketminds", tags=["marketminds"])
