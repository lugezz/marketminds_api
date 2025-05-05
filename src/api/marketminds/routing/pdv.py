from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select

from api.db.session import get_session
from api.helpers.tools import dict_all_serialized
from api.marketminds.models import PDV


pdv_router = APIRouter()
session = next(get_session())


@pdv_router.get("/pdv", response_model=list[dict])
def get_pdv():
    """
    Get all Punto de Venta (PDV)
    """
    stmt = (
        select(
            PDV.id,
            PDV.cod_pdv,
            PDV.ubicacion,
        )
    )

    all_pdv = session.execute(stmt).all()
    pdvs = []
    for pdv in all_pdv:
        pdv_dict = {
            "id": pdv.id,
            "code": pdv.cod_pdv,
            "ubicacion": pdv.ubicacion,
            "pois_count": pdv.pois_count,
        }

        pdvs.append(pdv_dict)

    return JSONResponse(content=pdvs, status_code=200)


@pdv_router.get("/pdv/{pdv_id}", response_model=dict)
def get_provincia(pdv_id: int):
    """
    Get a Punto de Venta (PDV) by ID.
    """
    pdv = session.query(PDV).filter(PDV.id == pdv_id).first()
    if not pdv:
        return JSONResponse(content={"error": "PDV not found"}, status_code=404)

    pdv_dict = pdv.dict()
    pdv_dict["pois_count"] = len(pdv.pois)
    pdv_ser_dict = dict_all_serialized(pdv_dict)

    return JSONResponse(content=pdv_ser_dict, status_code=200)
