import logging

import pandas as pd
from sqlmodel import select

from api.db.session import get_session
from api.marketminds.models import (
    CanalDistribucion,
    Categoria,
    Client,
    Departamento,
    GerenteNacional,
    GerenteRegional,
    PDV,
    # POI,
    # POISType,
    Provincia,
    SubcanalAdicional,
    Sucursal,
    Vendedor,
)
from api.helpers.tools import get_datetime_from_str, si_no_a_bool

logger = logging.getLogger(__name__)
session = next(get_session())

pdv_keys_dict = {
    'id': {'name': 'id_pdv_unique'},
    'cod_pdv': {'name': 'id_cod_pdv'},
    'fecha_alta': {'name': 'id_tie_fecha_alta'},
    'lat': {'name': 'pv_y'},
    'lon': {'name': 'pv_x'},
    'geohash': {'name': 'geohash'},
    'bandejas': {'name': 'indicar_cantidad_de_bandejas'},
    'm2': {'name': 'indique_la_cantidad_de_m2_de_la_tienda'},
    'pasillos': {'name': 'indique_la_cantidad_de_pasillos'},
    'puertas_heladeras': {'name': 'indique_la_cantidad_de_puertas_de_heladeras'},
    'puntos_cobro': {'name': 'indique_la_cantidad_de_puntos_de_cobro_cajas_del_pdv'},
    'tiene_ingreso': {'name': 'se_puede_ingresar_al_interior_del_local', 'type': 'bool'},
    'compra_en_plataformas': {
        'name': 'compra_en_plataformas_web_ej_bees_compre_ahora_coca_tokin',
        'type': 'bool',
    },
    'cuenta_con_apps_delivery': {
        'name': 'cuenta_con_apps_de_delivery_ej_pedidos_ya_rappi_propia',
        'type': 'bool',
    },
    'cuenta_con_deposito': {
        'name': 'cuenta_con_deposito_de_mercaderia',
        'type': 'bool',
    },
    'cuenta_con_medios_cobro_digital': {
        'name': 'cuenta_con_medios_de_cobro_digital_o_electronico_ej_posnet_apps_de_pago_qr',
        'type': 'bool',
    },
    'otros_servicios': {
        'name': 'cuenta_con_otros_servicios_ej_tarjeta_colectivos_carga_celular_cospeles_rapipago_pago_facil',
        'type': 'bool',
    },
    'ubicacion': {'name': 'donde_se_encuentra_ubicado'},
    'abierto_24h': {'name': 'la_tienda_se_encuentra_abierta_las_24_hs_del_dia', 'type': 'bool'},
    'abierto_7d': {'name': 'la_tienda_se_encuentra_abierta_los_7_dias_de_la_semana', 'type': 'bool'},
    'bebidas_alcoholicas': {'name': 'ofrece_bebidas_alcoholicas', 'type': 'bool'},
    'medicamentos_venta_libre': {
        'name': 'ofrece_medicamentos_de_venta_libre_ej_ibuprofeno_sertal_otros',
        'type': 'bool'
    },
    'cuidados_personales': {
        'name': 'ofrece_producto_de_cuidado_personal_ej_shampoo_maquinita_de_afeitar_toallitas_femeninas',
        'type': 'bool'
    },
    'productos_lacteos': {'name': 'ofrece_productos_lacteos', 'type': 'bool'},
    'productos_varios': {'name': 'ofrece_productos_varios_ej_pilas_encendedroes_preservativos', 'type': 'bool'},
    'viandas': {'name': 'ofrece_viandas_ej_menues_tartas_sandwiches_ensaladas', 'type': 'bool'},
    'freezer': {'name': 'tiene_freezer_cual_es'},
    'imagen_frente': {'name': 'tiene_imagen_en_el_frente_del_local', 'type': 'bool'},
    'presencia_redes_sociales': {
        'name': 'tiene_presencia_en_redes_sociales_ej_instagram_facebook_tik_tok',
        'type': 'bool'
    },
    'eventos_tematicos': {
        'name': 'trabaja_los_eventos_tematicos_navidad_pascuas_halloween_seleccion_argentina',
        'type': 'bool'
    },
}


def get_clients_dict() -> dict[str, Client]:
    clients = session.exec(select(Client)).all()
    return {str(client.id): client for client in clients}


def get_any_model_dict(model_to_get, this_key: str = 'id') -> dict[str, any]:
    """
    Devuelve un diccionario de un modelo específico.
    :param model_to_get: El modelo del cual se quiere obtener los ids.
    :return: Un diccionario con los ids del modelo.
    """
    # Obtener todos los registros del modelo
    all_records = session.query(model_to_get).all()

    # Crear un diccionario con los ids
    records_dict = {getattr(record, this_key): record for record in all_records}
    return records_dict


def get_set_of_ids(model_to_get, this_key: str = 'id') -> set:
    """
    Devuelve un set de ids de un modelo específico.
    :param model_to_get: El modelo del cual se quiere obtener los ids.
    :return: Un set con los ids del modelo.
    """
    # Obtener todos los registros del modelo
    all_records = session.query(model_to_get).all()

    # Crear un set con los ids
    ids = {getattr(record, this_key) for record in all_records}
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


def get_set_of_departamentos_names() -> set:
    """
    Devuelve un set de names de departamento
    :return: Un set con "provincia_id - name" de departamentos.
    """
    # Obtener todos los registros del modelo
    all_records = session.query(Departamento).all()

    # Crear un set con los ids
    names = {f"{record.provincia_id} - {record.name}" for record in all_records}
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
    names_set: set,
    model_class,
    instance_related,
    related_key: str,
    related_instance: str,
):
    """
    Procesa un registro de un modelo que sólo tiene un nombre relacionado con otro modelo, a buscar por name.
    :param row: La fila del DataFrame.
    :param name_key: La clave del nombre en el DataFrame.
    :param model_class: La clase del modelo a procesar.
    :param model_class_related: La clase del modelo relacionado a procesar.
    :return: None si no crea o registro creado
    :param related_name: El nombre del campo relacionado en el modelo.
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
        new_registro_params = {
            'name': name_value,
            related_key: instance_related.id,
            related_instance: instance_related,
        }
        this_registro = model_class(**new_registro_params)

    return this_registro


def process_base_model(
    row,
    id_key: str,
    name_key: str,
    ids_set: set,
    model_class,
    this_client,
    models_to_import: list,
):
    new_record = process_any_id_name_pair(
        row=row,
        id_key=id_key,
        name_key=name_key,
        ids_set=ids_set,
        model_class=model_class,
    )

    if new_record:
        new_record.client_id = this_client.id
        new_record.client = this_client
        models_to_import.append(new_record)
        ids_set.add(str(row[id_key]))

    return new_record


def process_pdv(
    row,
    ids_set: set,
    this_client,
    models_to_import: list,
):
    if str(row['id_pdv_unique']) in ids_set:
        # Si el pdv ya existe, no lo creo
        return None

    pdv_data = {
        'client_id': this_client.id,
        'client': this_client,
    }

    for key, value in pdv_keys_dict.items():
        dataset_key = value['name']

        if dataset_key in row:
            if value.get('type') == 'bool':
                pdv_data[key] = si_no_a_bool(row[dataset_key])
            elif value.get('type') == 'int':
                pdv_data[key] = int(row[dataset_key]) if not pd.isna(row[dataset_key]) else 0
            else:
                pdv_data[key] = str(row[dataset_key])
        else:
            pdv_data[key] = None

    # Limpieza algunos campos
    pdv_data['fecha_alta'] = get_datetime_from_str(pdv_data['fecha_alta'])

    # Creo el pdv
    new_pdv = PDV(**pdv_data)
    models_to_import.append(new_pdv)
    ids_set.add(str(row['id_pdv_unique']))

    return new_pdv


def process_provincia_departamento(
    row,
    models_to_import: list,
    provincias_dict: dict,
    names_provincia: set,
    names_departamento: set,
):
    """
    Procesa un registro de provincia y departamento.
    :param row: La fila del DataFrame.
    :param models_to_import: La lista de modelos a importar.
    :param provincias_dict: El diccionario de provincias.
    :param names_provincia: El set de nombres de provincias.
    :param names_departamento: El set de nombres de departamentos.
    :return: None
    """
    provincia_name = row["pv_pcia"]
    if provincia_name not in names_provincia:
        new_provincia = process_just_name(
            row,
            name_key="pv_pcia",
            names_set=names_provincia,
            model_class=Provincia,
        )
        if new_provincia:
            # En el caso de provincia lo grabo ahora ya que necesito vincularlo a departamento
            session.add(new_provincia)
            session.commit()
            provincias_dict[provincia_name] = new_provincia
            names_provincia.add(provincia_name)
    else:
        new_provincia = provincias_dict[provincia_name]

    # Departamento --------------------------------------
    departamento_name = row["pv_departamento"]
    prov_departamento_name = f"{new_provincia.id} - {departamento_name}"
    if prov_departamento_name not in names_departamento:
        new_departamento = process_related_names(
            row,
            name_key="pv_departamento",
            names_set=names_departamento,
            model_class=Departamento,
            instance_related=new_provincia,
            related_key="provincia_id",
            related_instance="provincia",
        )
        if new_departamento:
            models_to_import.append(new_departamento)
            names_departamento.add(prov_departamento_name)


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
    initial_canal_distribucion = get_set_of_ids(CanalDistribucion)
    ids_canal_distribucion = initial_canal_distribucion.copy()
    initial_categoria = get_set_of_ids(Categoria)
    ids_categoria = initial_categoria.copy()
    provincias_dict = get_any_model_dict(Provincia, "name")
    initial_provincia = set(list(provincias_dict.keys()))
    names_provincia = initial_provincia.copy()
    initial_departamento = get_set_of_names(Departamento)
    names_departamento = initial_departamento.copy()
    initial_gerente_nacional = get_set_of_ids(GerenteNacional)
    ids_gerente_nacional = initial_gerente_nacional.copy()
    initial_gerente_regional = get_set_of_ids(GerenteRegional)
    ids_gerente_regional = initial_gerente_regional.copy()
    initial_sucursal = get_set_of_ids(Sucursal)
    ids_sucursal = initial_sucursal.copy()
    initial_subcanal_adicional = get_set_of_ids(SubcanalAdicional)
    ids_subcanal_adicional = initial_subcanal_adicional.copy()
    initial_vendedor = get_set_of_ids(Vendedor)
    ids_vendedor = initial_vendedor.copy()
    initial_pdv = get_set_of_ids(PDV)
    ids_pdv = initial_pdv.copy()

    # -------------------------------------------------------------------------------------

    # Procesar cada fila del DataFrame
    for index, row in df.iterrows():
        if index == 0:
            # Skip the first row if it contains headers or unwanted data
            continue
        # Crear instancias de los modelos y asignar valores ------------------------------------
        # Client -------------------------------------------------------------
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
                model_class=Client
            )
            if new_client:
                models_to_import.append(new_client)
                ids_client.add(str(row["id_cli_suc_cuenta"]))
            this_cliente = new_client
            clients_dict[this_cliente_id] = new_client
        else:
            this_cliente = clients_dict[this_cliente_id]

        # Fin Client -------------------------------------------------------------

        # CanalDistribucion -----------------------------
        process_base_model(
            row=row,
            id_key="id_cli_canal_dist",
            name_key="desc_cli_canal_dist",
            ids_set=ids_canal_distribucion,
            model_class=CanalDistribucion,
            models_to_import=models_to_import,
            this_client=this_cliente,
        )

        # Categoría ------------------------------------------
        process_base_model(
            row=row,
            id_key="id_cli_categoria_dist",
            name_key="(Sin nombre)",
            ids_set=ids_categoria,
            model_class=Categoria,
            models_to_import=models_to_import,
            this_client=this_cliente,
        )

        # Provincias y Departamentos -------------------------------------
        process_provincia_departamento(
            row=row,
            models_to_import=models_to_import,
            provincias_dict=provincias_dict,
            names_provincia=names_provincia,
            names_departamento=names_departamento,
        )

        # Gerente Nacional --------------------------------
        process_base_model(
            row=row,
            id_key="id_cli_gte_nacional",
            name_key="desc_cli_gte_nacional",
            ids_set=ids_gerente_nacional,
            model_class=GerenteNacional,
            this_client=this_cliente,
            models_to_import=models_to_import,
        )

        # Gerente Regional --------------------------------
        process_base_model(
            row=row,
            id_key="id_cli_gte_regional",
            name_key="desc_cli_gte_regional",
            ids_set=ids_gerente_regional,
            model_class=GerenteRegional,
            this_client=this_cliente,
            models_to_import=models_to_import,
        )

        # Sucursal --------------------------------------
        process_base_model(
            row=row,
            id_key="id_cli_suc_cuenta",
            name_key="desc_cli_suc_cuenta",
            ids_set=ids_sucursal,
            model_class=Sucursal,
            this_client=this_cliente,
            models_to_import=models_to_import,
        )

        # Subcanal Adicional -----------------------------
        process_base_model(
            row=row,
            id_key="id_cli_subcanal_adic_dist",
            name_key="desc_cli_subcanal_dist",
            ids_set=ids_subcanal_adicional,
            model_class=SubcanalAdicional,
            this_client=this_cliente,
            models_to_import=models_to_import,
        )

        # Vendedor --------------------------------------
        process_base_model(
            row=row,
            id_key="id_cli_vendedor",
            name_key="desc_cli_vendedor",
            ids_set=ids_vendedor,
            model_class=Vendedor,
            this_client=this_cliente,
            models_to_import=models_to_import,
        )

        # PDV ------------------------------------------------
        process_pdv(
            row=row,
            ids_set=ids_pdv,
            this_client=this_cliente,
            models_to_import=models_to_import,
        )

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
        "pdv": len(ids_pdv) - len(initial_pdv),
        # "poi_type": len(ids_poi_type),
        # "poi": len(ids_poi),
        "subcanal_adicional": len(ids_subcanal_adicional) - len(initial_subcanal_adicional),
        "sucursal": len(ids_sucursal) - len(initial_sucursal),
        "vendedor": len(ids_vendedor) - len(initial_vendedor),
    }

    # Cerrar la sesión
    session.close()

    return resp
