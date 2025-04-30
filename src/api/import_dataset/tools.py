import logging

import pandas as pd
from sqlmodel import select

from api.db.session import get_session
from api.marketminds.models import (
    CanalDistribucionModel,
    CategoriaModel,
    ClientModel,
    DepartamentoModel,
    GerenteNacionalModel,
    GerenteRegionalModel,
    # PDVModel,
    # POIModel,
    # POISTypeModel,
    ProvinciaModel,
    SubcanalAdicionalModel,
    SucursalModel,
    VendedorModel,
)

logger = logging.getLogger(__name__)

session = next(get_session())


def get_clients_dict() -> dict[str, ClientModel]:
    clients = session.exec(select(ClientModel)).all()
    return {str(client.id): client for client in clients}


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


def process_related_names(
    row,
    name_key: str,
    related_name: str,
    names_set: set,
    model_class,
    model_class_related,
    id_related_field: str,
    instance_related: str,
):
    """
    Procesa un registro de un modelo que sólo tiene un nombre relacionado con otro modelo, a buscar por name.
    :param row: La fila del DataFrame.
    :param name_key: La clave del nombre en el DataFrame.
    :param related_name: La clave del nombre relacionado en el DataFrame.
    :param model_class: La clase del modelo a procesar.
    :param model_class_related: La clase del modelo relacionado a procesar.
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
        related_name_value = row[related_name]
        related_registro = session.query(
            model_class_related
        ).filter(
            model_class_related.name == related_name_value
        ).first()
        if related_registro is None:
            # Si no existe el registro relacionado, lo creo
            related_registro = model_class_related(
                name=related_name_value,
            )
            session.add(related_registro)
            session.commit()
        # Sólo agregar si nombre si no es nulo y no está en el set
        new_registro_params = {
            id_related_field: related_registro.id,
            instance_related: related_registro,
        }
        new_registro_params['name'] = name_value
        this_registro = model_class(**new_registro_params)

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
    clients_dict = get_clients_dict()
    initial_client = set(list(clients_dict.keys()))
    ids_client = initial_client.copy()
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
    initial_gerente_regional = get_set_of_ids(GerenteRegionalModel)
    ids_gerente_regional = initial_gerente_regional.copy()
    initial_sucursal = get_set_of_ids(SucursalModel)
    ids_sucursal = initial_sucursal.copy()
    initial_subcanal_adicional = get_set_of_ids(SubcanalAdicionalModel)
    ids_subcanal_adicional = initial_subcanal_adicional.copy()
    initial_vendedor = get_set_of_ids(VendedorModel)
    ids_vendedor = initial_vendedor.copy()
    # -------------------------------------------------------------------------------------

    # Procesar cada fila del DataFrame
    for index, row in df.iterrows():
        if index == 0:
            # Skip the first row if it contains headers or unwanted data
            continue
        # Crear instancias de los modelos y asignar valores ------------------------------------
        # ClientModel -------------------------------------------------------------
        # Por ahora tomo a cliente como id_cli_suc_cuenta y desc_cli_suc_cuenta
        # A futuro definir como mejorar si un cliente tiene sucursales
        # Id = -1 para clientes no identificados
        this_cliente_id = str(row["id_cli_suc_cuenta"])
        if this_cliente_id not in ids_client:
            new_client = process_any_id_name_pair(
                row,
                id_key="id_cli_suc_cuenta",
                name_key="desc_cli_suc_cuenta",
                ids_set=ids_client,
                model_class=ClientModel
            )
            if new_client:
                models_to_import.append(new_client)
                ids_client.add(str(row["id_cli_suc_cuenta"]))
            this_cliente = new_client
            clients_dict[this_cliente_id] = new_client
        else:
            this_cliente = clients_dict[this_cliente_id]

        # Fin ClientModel -------------------------------------------------------------

        # CanalDistribucionModel -----------------------------
        new_canal = process_any_id_name_pair(
            row,
            id_key="id_cli_canal_dist",
            name_key="desc_cli_canal_dist",
            ids_set=ids_canal_distribucion,
            model_class=CanalDistribucionModel,
        )

        if new_canal:
            new_canal.client_id = this_cliente_id
            new_canal.client = this_cliente
            models_to_import.append(new_canal)
            ids_canal_distribucion.add(str(row["id_cli_canal_dist"]))

        # Categoría ------------------------------------------
        new_categoria = process_any_id_name_pair(
            row,
            id_key="id_cli_categoria_dist",
            name_key="(Sin nombre)",
            ids_set=ids_categoria,
            model_class=CategoriaModel,
        )
        if new_categoria:
            new_categoria.client_id = this_cliente_id
            new_categoria.client = this_cliente
            models_to_import.append(new_categoria)
            ids_categoria.add(str(row["id_cli_categoria_dist"]))

        # Provincia --------------------------------------
        new_provincia = process_just_name(
            row,
            name_key="pv_pcia",
            names_set=names_provincia,
            model_class=ProvinciaModel,
        )
        if new_provincia:
            # En el caso de provincia lo grabo ahora ya que necesito vincularlo a departamento
            session.add(new_provincia)
            session.commit()

        # Departamento --------------------------------------
        departamento_name = row["pv_departamento"]
        if departamento_name not in names_departamento:
            new_departamento = process_related_names(
                row,
                name_key="pv_departamento",
                related_name="pv_pcia",
                names_set=names_departamento,
                model_class=DepartamentoModel,
                model_class_related=ProvinciaModel,
                id_related_field="provincia_id",
                instance_related="provincia",
            )
            if new_departamento:
                models_to_import.append(new_departamento)
                names_departamento.add(departamento_name)

        # Gerente Nacional --------------------------------
        new_gerente_nacional = process_any_id_name_pair(
            row,
            id_key="id_cli_gte_nacional",
            name_key="desc_cli_gte_nacional",
            ids_set=ids_gerente_nacional,
            model_class=GerenteNacionalModel,
        )
        if new_gerente_nacional:
            new_gerente_nacional.client_id = this_cliente_id
            new_gerente_nacional.client = this_cliente
            models_to_import.append(new_gerente_nacional)
            ids_gerente_nacional.add(str(row["id_cli_gte_nacional"]))

        # Gerente Regional --------------------------------
        new_gerente_regional = process_any_id_name_pair(
            row,
            id_key="id_cli_gte_regional",
            name_key="desc_cli_gte_regional",
            ids_set=ids_gerente_regional,
            model_class=GerenteRegionalModel,
        )
        if new_gerente_regional:
            new_gerente_regional.client_id = this_cliente_id
            new_gerente_regional.client = this_cliente
            models_to_import.append(new_gerente_regional)
            ids_gerente_regional.add(str(row["id_cli_gte_regional"]))

        # Sucursal --------------------------------------
        new_sucursal = process_any_id_name_pair(
            row,
            id_key="id_cli_suc_cuenta",
            name_key="desc_cli_suc_cuenta",
            ids_set=ids_sucursal,
            model_class=SucursalModel,
        )
        if new_sucursal:
            new_sucursal.client_id = this_cliente_id
            new_sucursal.client = this_cliente
            models_to_import.append(new_sucursal)
            ids_sucursal.add(str(row["id_cli_suc_cuenta"]))

        # Subcanal Adicional -----------------------------
        new_subcanal_adicional = process_any_id_name_pair(
            row,
            id_key="id_cli_subcanal_adic_dist",
            name_key="desc_cli_subcanal_dist",
            ids_set=ids_subcanal_adicional,
            model_class=SubcanalAdicionalModel,
        )
        if new_subcanal_adicional:
            new_subcanal_adicional.client_id = this_cliente_id
            new_subcanal_adicional.client = this_cliente
            models_to_import.append(new_subcanal_adicional)
            ids_subcanal_adicional.add(str(row["id_cli_subcanal_adic_dist"]))

        # Vendedor --------------------------------------
        new_vendedor = process_any_id_name_pair(
            row,
            id_key="id_cli_vendedor",
            name_key="desc_cli_vendedor",
            ids_set=ids_vendedor,
            model_class=VendedorModel,
        )
        if new_vendedor:
            new_vendedor.client_id = this_cliente_id
            new_vendedor.client = this_cliente
            models_to_import.append(new_vendedor)
            ids_vendedor.add(str(row["id_cli_vendedor"]))

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

    # Agregar las instancias a la sesión
    session.add_all(models_to_import)
    session.commit()

    resp['registros_added'] = {
        "canal_distribucion": len(ids_canal_distribucion) - len(initial_canal_distribucion),
        "categoria": len(ids_categoria) - len(initial_categoria),
        "client": len(ids_client) - len(initial_client),
        "provincia": len(names_provincia) - len(initial_provincia),
        "departamento": len(names_departamento) - len(initial_departamento),
        "gerente_nacional": len(ids_gerente_nacional) - len(initial_gerente_nacional),
        "gerente_regional": len(ids_gerente_regional) - len(initial_gerente_regional),
        # "pdv": len(ids_pdv),
        # "poi_type": len(ids_poi_type),
        # "poi": len(ids_poi),
        "subcanal_adicional": len(ids_subcanal_adicional) - len(initial_subcanal_adicional),
        "sucursal": len(ids_sucursal) - len(initial_sucursal),
        "vendedor": len(ids_vendedor) - len(initial_vendedor),
    }

    # Cerrar la sesión
    session.close()

    return resp
