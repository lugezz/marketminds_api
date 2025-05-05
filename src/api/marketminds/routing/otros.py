from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.db.session import get_session
from api.helpers.tools import dict_all_serialized
from api.marketminds.models import (
    CanalDistribucion,
    Categoria,
    Client,
    GerenteNacional,
    GerenteRegional,
    SubcanalAdicional,
    Sucursal,
    Vendedor,
)


otros_router = APIRouter()
session = next(get_session())


def base_get_all(model_class):
    """
    Base function to get all records from a model.
    """
    all_records = session.query(model_class).all()
    records = []
    for record in all_records:
        record_dict = record.dict()
        record_ser_dict = dict_all_serialized(record_dict)
        records.append(record_ser_dict)

    return JSONResponse(content=records, status_code=200)


@otros_router.get("/canales-distribucion", response_model=list[dict])
def get_canales_distribucion():
    """
    Get all Canales de Distribución.
    """
    return base_get_all(CanalDistribucion)


@otros_router.get("/categorias", response_model=list[dict])
def get_categorias():
    """
    Get all Categorías.
    """
    return base_get_all(Categoria)


@otros_router.get("/clientes", response_model=list[dict])
def get_clientes():
    """
    Get all Clientes.
    """
    return base_get_all(Client)


@otros_router.get("/gerentes-nacionales", response_model=list[dict])
def get_gerentes_nacionales():
    """
    Get all Gerentes Nacionales.
    """
    return base_get_all(GerenteNacional)


@otros_router.get("/gerentes-regionales", response_model=list[dict])
def get_gerentes_regionales():
    """
    Get all Gerentes Regionales.
    """
    return base_get_all(GerenteRegional)


@otros_router.get("/subcanales-adicionales", response_model=list[dict])
def get_subcanales_adicionales():
    """
    Get all Subcanales Adicionales.
    """
    return base_get_all(SubcanalAdicional)


@otros_router.get("/sucursales", response_model=list[dict])
def get_sucursales():
    """
    Get all Sucursales.
    """
    return base_get_all(Sucursal)


@otros_router.get("/vendedores", response_model=list[dict])
def get_vendedores():
    """
    Get all Vendedores.
    """
    return base_get_all(Vendedor)
