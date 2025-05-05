from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.db.session import get_session
from api.marketminds.models import Departamento, Provincia


prov_router = APIRouter()
session = next(get_session())


@prov_router.get("/provincias", response_model=list[dict])
def get_provincias():
    """
    Get all provinces.
    """
    all_provincias = session.query(Provincia).all()
    provincias = []
    for provincia in all_provincias:
        provincias.append({
            "id": provincia.id,
            "name": provincia.name,
            "departamentos_count": len(provincia.departamentos),
        })

    return JSONResponse(content=provincias, status_code=200)


@prov_router.get("/provincias/{provincia_id}", response_model=dict)
def get_provincia(provincia_id: int):
    """
    Get a province by ID.
    """
    provincia = session.query(Provincia).filter(Provincia.id == provincia_id).first()
    if not provincia:
        return JSONResponse(content={"error": "Province not found"}, status_code=404)

    return JSONResponse(content={
        "id": provincia.id,
        "name": provincia.name,
        "departamentos_count": len(provincia.departamentos),
    }, status_code=200)


@prov_router.get("/departamentos", response_model=list[dict])
def get_departamentos():
    """
    Get all departments.
    """
    all_departamentos = session.query(Departamento).all()
    departamentos = []
    for departamento in all_departamentos:
        departamentos.append({
            "id": departamento.id,
            "name": departamento.name,
            "provincia_id": departamento.provincia_id,
        })

    return JSONResponse(content=departamentos, status_code=200)
