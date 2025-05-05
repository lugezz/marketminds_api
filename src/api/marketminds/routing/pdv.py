from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select

from api.db.session import get_session
from api.helpers.tools import dict_all_serialized
from api.marketminds.models import PDV, POISType, POIAndPDV


pdv_router = APIRouter()
session = next(get_session())


@pdv_router.get("/pdv", response_model=list[dict])
def get_pdvs():
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
        }

        pdvs.append(pdv_dict)

    return JSONResponse(content=pdvs, status_code=200)


@pdv_router.get("/pdv/{pdv_id}", response_model=dict)
def get_pdv(pdv_id: int):
    """
    Get a Punto de Venta (PDV) by ID.
    """
    pdv = session.query(PDV).filter(PDV.id == pdv_id).first()
    if not pdv:
        return JSONResponse(content={"error": "PDV not found"}, status_code=404)

    pdv_dict = pdv.dict()
    pdv_ser_dict = dict_all_serialized(pdv_dict)

    return JSONResponse(content=pdv_ser_dict, status_code=200)


@pdv_router.get("/pois-types", response_model=list[str])
def get_pois_types():
    """
    Get all POI types.
    """
    all_pois_types = session.query(POISType).all()
    pois_types = []
    for pois_type in all_pois_types:
        pois_types.append(pois_type.name)

    return JSONResponse(content=pois_types, status_code=200)


def get_poi_type_name_by_id(poi_type_id: int) -> str:
    """
    Get POI type name by ID.
    """
    poi_type = session.query(POISType).filter(POISType.id == poi_type_id).first()
    if not poi_type:
        return "Unknown"
    return poi_type.name


@pdv_router.get("/pois-for-pdv/{pdv_id}", response_model=list[dict])
def get_pois_for_pdv(pdv_id: str):
    """
    Get all POIs for a given PDV.
    """
    pois = session.query(POIAndPDV).filter(POIAndPDV.pdv_id == pdv_id).all()
    pois_list = []
    for poi in pois:
        poi_dict = poi.dict()
        poi_type_id = poi_dict.pop("pois_type_id")
        poi_type_name = get_poi_type_name_by_id(poi_type_id)
        poi_dict["poi_type"] = poi_type_name
        poi_ser_dict = dict_all_serialized(poi_dict)
        pois_list.append(poi_ser_dict)

    return JSONResponse(content=pois_list, status_code=200)
