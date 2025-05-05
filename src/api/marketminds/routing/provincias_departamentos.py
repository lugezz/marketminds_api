from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.db.session import get_session
# from api.marketminds.models import Departamento, Provincia


prov_router = APIRouter()
session = next(get_session())


@prov_router.get("/provincias", response_model=list[dict])
def get_provincias():
    """
    Get all provinces.
    """
    try:
        query = session.execute("SELECT * FROM provincias")
        provincias = query.fetchall()
        return JSONResponse(content=[dict(row) for row in provincias])
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
