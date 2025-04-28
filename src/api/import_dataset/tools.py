import logging

import pandas as pd

from api.db.session import get_session
from api.marketminds.models import (
    CanalDistribucionModel,
    CategoriaModel,
    DepartamentoModel,
    GerenteNacionalModel,
    GerenteRegionalModel,
    PDVModel,
    POIModel,
    POISTypeModel,
    ProvinciaModel,
    SubcanalAdicionalModel,
    SucursalModel,
    VendedorModel,
)

logger = logging.getLogger(__name__)


def import_dataset():
    # Toma el archivo de import (api/datasets/mdt_negocio_import.csv), lo convierte a un dataframe 
    # y lo va procesando en los modelos de la base de datos.

    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv("api/datasets/mdt_negocio_import.csv", encoding="utf-8")

    # Crear una sesión de base de datos
    session = next(get_session())
    models_to_import = []

    # Sets de ids para evitar duplicados
    ids_canal_distribucion = set()

    # Procesar cada fila del DataFrame
    for index, row in df.iterrows():
        if index == 0:
            # Skip the first row if it contains headers or unwanted data
            continue
        # Crear instancias de los modelos y asignar valores ------------------------------------
        # CanalDistribucionModel -----------------------------
        id_cli_canal_dist = row["id_cli_canal_dist"]
        desc_cli_canal_dist = row["desc_cli_canal_dist"]

        if (
            id_cli_canal_dist not in ids_canal_distribucion or
            pd.isna(id_cli_canal_dist) or
            pd.isna(desc_cli_canal_dist)
        ):
            # Sólo agregar si el id y la descripción no son nulos y no están en el set
            canal_distribucion = CanalDistribucionModel(
                id=id_cli_canal_dist,
                name=desc_cli_canal_dist,
            )
            models_to_import.append(canal_distribucion)
            ids_canal_distribucion.add(id_cli_canal_dist)

        # categoria = CategoriaModel(
        #     id=row["categoria_id"],
        #     nombre=row["categoria_nombre"],
        # )
        # departamento = DepartamentoModel(
        #     id=row["departamento_id"],
        #     nombre=row["departamento_nombre"],
        # )
        # gerente_nacional = GerenteNacionalModel(
        #     id=row["gerente_nacional_id"],
        #     nombre=row["gerente_nacional_nombre"],
        # )
        # gerente_regional = GerenteRegionalModel(
        #     id=row["gerente_regional_id"],
        #     nombre=row["gerente_regional_nombre"],
        # )
        # pdv = PDVModel(
        #     id=row["pdv_id"],
        #     nombre=row["pdv_nombre"],
        # )
        # poi_type = POISTypeModel(
        #     id=row["poi_type_id"],
        #     nombre=row["poi_type_nombre"],
        # )
        # poi = POIModel(
        #     id=row["poi_id"],
        #     nombre=row["poi_nombre"],
        # )
        # provincia = ProvinciaModel(
        #     id=row["provincia_id"],
        #     nombre=row["provincia_nombre"],
        # )
        # subcanal_adicional = SubcanalAdicionalModel(
        #     id=row["subcanal_adicional_id"],
        #     nombre=row["subcanal_adicional_nombre"],
        # )
        # sucursal = SucursalModel(
        #     id=row["sucursal_id"],
        #     nombre=row["sucursal_nombre"],
        # )
        # vendedor = VendedorModel(
        #     id=row["vendedor_id"],
        #     nombre=row["vendedor_nombre"],
        # )

        # Agregar las instancias a la sesión
        print("Se está importando el modelo canal_distribucion", "Cantidad registros: ", len(models_to_import))
        session.add_all(models_to_import)
        # session.add(categoria)
        # session.add(departamento)
        # session.add(gerente_nacional)
        # session.add(gerente_regional)
        # session.add(pdv)
        # session.add(poi_type)
        # session.add(poi)
        # session.add(provincia)

        session.commit()
