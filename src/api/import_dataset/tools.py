import logging

import pandas as pd

from api.db.session import get_session
from api.marketminds.models import (
    CanalDistribucionModel,
    CategoriaModel,
    DepartamentoModel,
    GerenteNacionalModel,
    # GerenteRegionalModel,
    # PDVModel,
    # POIModel,
    # POISTypeModel,
    ProvinciaModel,
    # SubcanalAdicionalModel,
    # SucursalModel,
    # VendedorModel,
)

logger = logging.getLogger(__name__)

session = next(get_session())


def get_set_of_ids(model_to_get) -> set:
    """
    Devuelve un set de ids de un modelo específico.
    :param model_to_get: El modelo del cual se quiere obtener los ids.
    :return: Un set con los ids del modelo.
    """
    # Obtener todos los registros del modelo
    all_records = session.query(model_to_get).all()

    # Crear un set con los ids
    ids = {record.id for record in all_records}
    return ids


def get_set_of_names(model_to_get) -> set:
    """
    Devuelve un set de names de un modelo específico.
    :param model_to_get: El modelo del cual se quiere obtener los names.
    :return: Un set con los names del modelo.
    """
    # Obtener todos los registros del modelo
    all_records = session.query(model_to_get).all()

    # Crear un set con los ids
    names = {record.name for record in all_records}
    return names


def process_any_id_name_pair(row, id_key: str, name_key: str, ids_set: set, model_class):
    """
    Procesa un par de id y nombre de cualquier modelo.
    :param row: La fila del DataFrame.
    :param id_key: La clave del id en el DataFrame.
    :param name_key: La clave del nombre en el DataFrame.
    :param model_class: La clase del modelo a procesar.
    :return: None si no crea o registro creado
    """
    id_value = str(row[id_key])
    if name_key == "(Sin nombre)":
        name_value = name_key
    else:
        name_value = str(row[name_key])

    this_registro = None
    if (
        id_value not in ids_set or
        pd.isna(id_value) or
        pd.isna(name_value)
    ):
        # Sólo agregar si el id y la descripción no son nulos y no están en el set
        this_registro = model_class(
            id=id_value,
            name=name_value,
        )

    return this_registro


def process_just_name(row, name_key: str, names_set: set, model_class):
    """
    Procesa un registro de un modelo que sólo tiene un nombre. (id es autonumérico)
    :param row: La fila del DataFrame.
    :param name_key: La clave del nombre en el DataFrame.
    :param model_class: La clase del modelo a procesar.
    :return: None si no crea o registro creado
    """
    if name_key == "(Sin nombre)":
        name_value = name_key
    else:
        name_value = row[name_key]

    this_registro = None
    if (
        name_value not in names_set or
        pd.isna(name_value)
    ):
        # Sólo agregar si nombre si no es nulo y no está en el set
        this_registro = model_class(
            name=name_value,
        )

    return this_registro


def import_dataset() -> dict:
    # Toma el archivo de import (api/datasets/mdt_negocio_import.csv), lo convierte a un dataframe
    # y lo va procesando en los modelos de la base de datos.
    resp = {
        "status": 200,
        "message": "Importación de dataset exitosa",
        "registros_added": {}
    }

    # Cargar el archivo CSV en un DataFrame de pandas
    df = pd.read_csv("api/datasets/mdt_negocio_import.csv", encoding="utf-8")

    # Crear una sesión de base de datos
    models_to_import = []

    # Sets de ids para evitar duplicados -------------------------------------------------
    initial_canal_distribucion = get_set_of_ids(CanalDistribucionModel)
    ids_canal_distribucion = initial_canal_distribucion.copy()
    initial_categoria = get_set_of_ids(CategoriaModel)
    ids_categoria = initial_categoria.copy()
    initial_provincia = get_set_of_names(ProvinciaModel)
    names_provincia = initial_provincia.copy()
    initial_departamento = get_set_of_names(DepartamentoModel)
    names_departamento = initial_departamento.copy()
    initial_gerente_nacional = get_set_of_ids(GerenteNacionalModel)
    ids_gerente_nacional = initial_gerente_nacional.copy()
    # -------------------------------------------------------------------------------------

    # Procesar cada fila del DataFrame
    for index, row in df.iterrows():
        if index == 0:
            # Skip the first row if it contains headers or unwanted data
            continue
        # Crear instancias de los modelos y asignar valores ------------------------------------
        # CanalDistribucionModel -----------------------------
        new_canal = process_any_id_name_pair(
            row,
            id_key="id_cli_canal_dist",
            name_key="desc_cli_canal_dist",
            ids_set=ids_canal_distribucion,
            model_class=CanalDistribucionModel,
        )

        if new_canal:
            models_to_import.append(new_canal)
            ids_canal_distribucion.add(str(new_canal.id))

        # Categoría ------------------------------------------
        new_categoria = process_any_id_name_pair(
            row,
            id_key="id_cli_categoria_dist",
            name_key="(Sin nombre)",
            ids_set=ids_categoria,
            model_class=CategoriaModel,
        )
        if new_categoria:
            models_to_import.append(new_categoria)
            ids_categoria.add(str(new_categoria.id))

        # Provincia --------------------------------------
        new_provincia = process_just_name(
            row,
            name_key="pv_pcia",
            names_set=names_provincia,
            model_class=ProvinciaModel,
        )
        if new_provincia:
            models_to_import.append(new_provincia)
            names_provincia.add(str(new_provincia.name))

        # Departamento --------------------------------------
        # new_departamento = process_any_id_name_pair(
        #     row,
        #     id_key="departamento_id",
        #     name_key="departamento_nombre",
        #     ids_set=ids_departamento,
        #     model_class=DepartamentoModel,
        # )

        # Gerente Nacional --------------------------------
        new_gerente_nacional = process_any_id_name_pair(
            row,
            id_key="id_cli_gte_nacional",
            name_key="desc_cli_gte_nacional",
            ids_set=ids_gerente_nacional,
            model_class=GerenteNacionalModel,
        )
        if new_gerente_nacional:
            models_to_import.append(new_gerente_nacional)
            ids_gerente_nacional.add(str(new_gerente_nacional.id))

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
    session.add_all(models_to_import)
    session.commit()

    resp['registros_added'] = {
        "canal_distribucion": len(ids_canal_distribucion) - len(initial_canal_distribucion),
        "categoria": len(ids_categoria) - len(initial_categoria),
        "provincia": len(names_provincia) - len(initial_provincia),
        "departamento": len(names_departamento) - len(initial_departamento),
        "gerente_nacional": len(ids_gerente_nacional) - len(initial_gerente_nacional),
        # "gerente_regional": len(ids_gerente_regional),
        # "pdv": len(ids_pdv),
        # "poi_type": len(ids_poi_type),
        # "poi": len(ids_poi),
        # "subcanal_adicional": len(ids_subcanal_adicional),
        # "sucursal": len(ids_sucursal),
        # "vendedor": len(ids_vendedor),
    }

    # Cerrar la sesión
    session.close()

    return resp
