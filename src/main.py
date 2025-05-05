from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.db.session import init_db
# Routing
from api.marketminds.routing.main import router as marketmind_router
from api.marketminds.routing.otros import otros_router
from api.marketminds.routing.pdv import pdv_router
from api.marketminds.routing.provincias_departamentos import prov_router


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

base_prefix = "/api/marketminds"
app.include_router(marketmind_router, prefix=base_prefix, tags=["marketminds"])
app.include_router(otros_router, prefix=base_prefix, tags=["otros"])
app.include_router(pdv_router, prefix=base_prefix, tags=["pdv"])
app.include_router(prov_router, prefix=base_prefix, tags=["provincias_departamentos"])
