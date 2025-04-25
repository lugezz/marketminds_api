from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import DateTime, Field, Relationship, SQLModel


def get_utc_now():
    """ Get current UTC datetime.
    """
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


class BaseModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, description="ID")
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        description="Creation timestamp",
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True),
        description="Update timestamp",
        nullable=False,
    )


"""
rename_columns = {
    'id_pdv_unique': 'Cod. PDV',
    'pois_agencias_de_viajes': 'POIS - Agencia de Viaje',
    'pois_alimentacion': 'POIS - Alimentación',
    'pois_alojamientos': 'POIS - Alojamiento',
    'pois_atracciones_turisticas': 'POIS - Atracciones Turisticas',
    'pois_bares_bodegas': 'POIS - Bares/Bodegas',
    'pois_centros_de_salud': 'POIS - Centro de Salud',
    'pois_clubes_deportivos': 'POIS - Clubes Deportivos',
    'pois_clubes_nocturnos': 'POIS - Clubes Nocturnos',
    'pois_escuelas': 'POIS -Escuelas',
    'pois_heladerias': 'POIS - Heladerias',
    'pois_hoteles': 'POIS - Hoteles',
    'pois_instituciones_educativas': 'POIS - Instituciones Educativas',
    'pois_otras_instituciones': 'POIS - Otras Instituciones',
    'pois_servicios_de_transporte': 'POIS - Transporte',
    'pois_bus_stop': 'POIS - Paradas de Bus',
    'total_pois': 'POIS - Totales',
    'total_pdvs_per_geohash': 'Total POIs en Geohash',
    'average_order_value': 'Ticket Promedio ($)',
    'total_sales': 'Ventas Totales ($)',
    'total_kgn': 'Ventas Totales (Kg)',
    'total_bultos': 'Ventas Totales (Bu)',
    'average_monthly_sales': 'Promedio Ventas Mensuales ($)',
    'average_active_monthly_sales': 'Promedio Ventas Meses Activos ($)',
    'deviation_monthly_sales': 'Desvio de Ventas Mensuales ($)',
    'average_monthly_kgn': 'Promedio Ventas Mensuales (Kg)',
    'average_active_monthly_kgn': 'Promedio Ventas Meses Activos (Kg)',
    'average_kgn_order': 'Ticket Promedio (Kg)',
    'omni_channel': 'Multicanal',
    'different_sku': 'SKU Diferentes',
    'ordenes_promedios_semanales_por_pdv': 'Ordenes Promedio Semanal',
    'buy_freq': 'Frecuencia de Compra Total',
    'buy_freq_hari_tostadas': 'Frecuencia de Compra Tostadas',
    'buy_freq_alimentos': 'Frecuencia de Compra Alimentos',
    'buy_freq_chocolates': 'Frecuencia de Compra Chocolate',
    'buy_freq_golosinas': 'Frecuencia de Compra Golosinas',
    'buy_freq_harinas': 'Frecuencia de Compra Harina',
    'fea_people_density_sqkm': 'Densidad Poblacional',
    'nse': 'Nivel Socioeconomico',
    'cantidad_exhibidores': 'Exhibidores',
    'cantidad_pasillos': 'Pasillos',
    'cantidad_proveedores': 'Proveedores',
    'cantidad_cajas': 'Cajas',
    'cantidad_heladeras': 'Heladeras',
    'tiene_ingreso': 'Ingreso',
    'metros2': 'Tamaño',
    'app_delivery': 'Delivery',
    'cobro_digital': 'Digital',
    'otros_servicios': 'Servicios',
    'en_esquina': 'Esquina',
    'abierto_24h': '24H',
    'vende_alcohol': 'Alcohol',
    'vende_productos_fraccionados': 'Fraccionados',
    'vende_productos_lacteos': 'Lacteos',
    'sobre_avenida': 'Avenida',
    'vende_productos_granel': 'Granel',
    'tiene_freezer': 'Freezer',
    'id_cli_suc_cuenta': 'ID Sucursal/Cuenta',
    'desc_cli_suc_cuenta': 'Sucursal/Cuenta',
    'id_tie_fecha_alta': 'Fecha de Alta',
    'pv_x': 'Latitud',
    'pv_y': 'Longitud',
    'desc_cli_canal_dist': 'Canal',
    'id_cli_categoria_dist': 'Categoria',
    'desc_cli_subcanal_dist': 'Subcanal',
    'pv_pcia': 'Provincia',
    'pv_departamento': 'Departamento',
    'geohash': 'Geohash',
    'desc_cli_vendedor': 'Jefe de Cuenta',
    'desc_cli_gte_regional': 'Gte. Regional',
    'desc_cli_gte_nacional': 'Gte. Nacional'
}
"""

"""
Columns:
(ok) id_pdv_unique
(ok) id_cli_suc_cuenta
(ok) id_cod_pdv
(ok) desc_cli_suc_cuenta
(ok) id_tie_fecha_alta
(ok) pv_x
(ok) pv_y
(ok) id_cli_canal_dist
(ok) desc_cli_canal_dist
(ok) id_cli_categoria_dist
(ok) id_cli_subcanal_adic_dist
(ok) desc_cli_subcanal_dist
(ok) pv_pcia
(ok) pv_departamento
(ok) geohash
(ok) id_cli_vendedor
(ok) desc_cli_vendedor
(ok) id_cli_gte_regional
(ok) desc_cli_gte_regional
(ok) id_cli_gte_nacional
(ok) desc_cli_gte_nacional
(ok) indicar_cantidad_de_bandejas
(ok) indique_la_cantidad_de_m2_de_la_tienda
(ok) indique_la_cantidad_de_pasillos
(ok) indique_la_cantidad_de_puertas_de_heladeras
(ok)
    indique_la_cantidad_de_puntos_de_cobro_cajas_del_pdv
    se_puede_ingresar_al_interior_del_local
    compra_en_plataformas_web_ej_bees_compre_ahora_coca_tokin
    cuenta_con_apps_de_delivery_ej_pedidos_ya_rappi_propia
    cuenta_con_deposito_de_mercaderia
    cuenta_con_medios_de_cobro_digital_o_electronico_ej_posnet_apps_de_pago_qr
    cuenta_con_otros_servicios_ej_tarjeta_colectivos_carga_celular_cospeles_rapipago_pago_facil
    donde_se_encuentra_ubicado
    la_tienda_se_encuentra_abierta_las_24_hs_del_dia
    la_tienda_se_encuentra_abierta_los_7_dias_de_la_semana
    ofrece_bebidas_alcoholicas
    ofrece_medicamentos_de_venta_libre_ej_ibuprofeno_sertal_otros
    ofrece_producto_de_cuidado_personal_ej_shampoo_maquinita_de_afeitar_toallitas_femeninas
    ofrece_productos_lacteos
    ofrece_productos_varios_ej_pilas_encendedroes_preservativos
    ofrece_viandas_ej_menues_tartas_sandwiches_ensaladas
    tiene_freezer_cual_es
    tiene_imagen_en_el_frente_del_local
    tiene_presencia_en_redes_sociales_ej_instagram_facebook_tik_tok
    trabaja_los_eventos_tematicos_navidad_pascuas_halloween_seleccion_argentina
(ok)
    pois_agencias_de_viajes
    pois_alimentacion
    pois_alojamientos
    pois_atracciones_turisticas
    pois_bares_bodegas
    pois_centros_de_salud
    pois_clubes_deportivos
    pois_clubes_nocturnos
    pois_escuelas
    pois_heladerias
    pois_hoteles
    pois_instituciones_educativas
    pois_otras_instituciones
    pois_servicios_de_transporte
    pois_bus_stop
    total_pois

Para ser calculados:
    total_pdvs_per_geohash
    average_order_value
    total_sales
    total_kgn
    total_bultos
    average_monthly_sales
    average_active_monthly_sales
    deviation_monthly_sales
    average_monthly_kgn
    average_active_monthly_kgn
    average_kgn_order
    omni_channel
    different_sku
    ordenes_promedios_semanales_por_pdv
    buy_freq
    buy_freq_alimentos
    buy_freq_chocolates
    buy_freq_golosinas
    buy_freq_harinas
    fea_people_density_sqkm
    nse_category
    cluster_sales
    cluster_geo
    cluster_size
    hubs_ps
    density_category
    total_sales_category
    total_kgn_category
    total_bultos_category
    average_monthly_sales_category
    average_monthly_kgn_category
    average_active_monthly_sales_category
    potencial
"""


# Provincias Model -----------------
class ProvinciaModel(BaseModel):
    """ Model for Provincias
    """

    name: str = Field(..., description="Nombre Provincia")
    departamentos: List["DepartamentoModel"] = Relationship(
        back_populates="provincia",
        sa_relationship_kwargs={"description": "Lista de Departamentos en esta Provincia"}
    )


# Departamentos Model -----------------
class DepartamentoModel(BaseModel):
    """ Model for Departamentos"""
    name: str = Field(..., description="Nombre Departamento")
    provincia_id: Optional[int] = Field(
        default=None,
        foreign_key="provinciamodel.id",
        description="Foreign key a ProvinciaModel"
    )
    provincia: Optional["ProvinciaModel"] = Relationship(
        back_populates="departamentos",
        sa_relationship_kwargs={"description": "Provincia relacionada con este Departamento"}
    )


# Models for PDV API -----------------
class PDVModel(BaseModel):
    cod_pdv: str = Field(..., description="Código PDV")
    name: str = Field(..., description="Nombre PDV")
    fecha_alta: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        description="Fecha de alta",
        nullable=True,
    )
    lat: float = Field(..., description="PDV latitud")
    lon: float = Field(..., description="PDV longitud")
    departamento_id: Optional[int] = Field(
        default=None,
        foreign_key="departamentomodel.id",
        description="Foreign key a DepartamentoModel"
    )
    pois: List["POIModel"] = Relationship(
        back_populates="pdv",
        sa_relationship_kwargs={"description": "Lista de POIs en este PDV"}
    )
    geohash: str = Field(..., description="Geohash del PDV")
    bandejas: Optional[int] = Field(default=None, description="Número de bandejas")
    m2: Optional[int] = Field(default=None, description="Número de m2")
    pasillos: Optional[int] = Field(default=None, description="Número de pasillos")
    puertas_heladeras: Optional[int] = Field(
        default=None,
        description="Número de puertas de heladeras"
    )
    puntos_cobro: Optional[int] = Field(
        default=None,
        description="Número de puntos de cobro (cajas)"
    )
    tiene_ingreso: Optional[bool] = Field(
        default=None,
        description="Tiene ingreso al interior del local"
    )
    compra_en_plataformas: Optional[bool] = Field(
        default=None,
        description="Compra en plataformas web (ej: BEES, Compre Ahora, Coca Tokin)"
    )
    cuenta_con_apps_delivery: Optional[bool] = Field(
        default=None,
        description="Cuenta con apps de delivery (ej: Pedidos Ya, Rappi, Propia)"
    )
    cuenta_con_deposito: Optional[bool] = Field(
        default=None,
        description="Cuenta con deposito de mercaderia"
    )
    cuenta_con_medios_cobro_digital: Optional[bool] = Field(
        default=None,
        description="Cuenta con medios de cobro digital o electronico (ej: Posnet, apps de pago QR)"
    )
    ubicacion: Optional[str] = Field(
        default=None,
        description="Ubicacion de la tienda"
    )
    abierto_24h: Optional[bool] = Field(
        default=False,
        description="La tienda se encuentra abierta las 24 hs del dia"
    )
    abierto_7d: Optional[bool] = Field(
        default=False,
        description="La tienda se encuentra abierta los 7 dias de la semana"
    )
    bebidas_alcoholicas: Optional[bool] = Field(
        default=False,
        description="Ofrece bebidas alcoholicas"
    )
    medicamentos_venta_libre: Optional[bool] = Field(
        default=False,
        description="Ofrece medicamentos de venta libre (ej: ibuprofeno, sertal, otros)"
    )
    cuidados_personales: Optional[bool] = Field(
        default=False,
        description="Ofrece producto de cuidado personal (ej: shampoo, maquinita de afeitar, toallitas femeninas)"
    )
    productos_lacteos: Optional[bool] = Field(
        default=False,
        description="Ofrece productos lacteos"
    )
    productos_varios: Optional[bool] = Field(
        default=False,
        description="Ofrece productos varios (ej: pilas, encendedores, preservativos)"
    )
    viandas: Optional[bool] = Field(
        default=False,
        description="Ofrece viandas (ej: menues, tartas, sandwiches, ensaladas)"
    )
    freezer: Optional[bool] = Field(
        default=False,
        description="Tiene freezer"
    )
    imagen_frente: Optional[bool] = Field(
        default=False,
        description="Tiene imagen en el frente del local"
    )
    presencia_redes_sociales: Optional[bool] = Field(
        default=False,
        description="Tiene presencia en redes sociales (ej: Instagram, Facebook, Tik Tok)"
    )
    eventos_tematicos: Optional[bool] = Field(
        default=False,
        description="Trabaja los eventos tematicos (navidad, pascuas, halloween, seleccion argentina)"
    )


class CreatePDVSchema(SQLModel):
    name: str = Field(..., description="Nombre PDV")
    fecha_alta: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        description="Fecha de alta",
        nullable=True,
    )
    lat: float = Field(..., description="PDV latitud")
    lon: float = Field(..., description="PDV longitud")
    departamento_id: Optional[int] = Field(
        default=None,
        foreign_key="departamentomodel.id",
        description="Foreign key a DepartamentoModel"
    )
    geohash: str = Field(..., description="Geohash del PDV")


class PDVListSchema(SQLModel):
    results: List[PDVModel] = Field(..., description="Listas de PDVs")
    count: int = Field(..., description="Total de PDVs")


class UpdatePDVSchema(SQLModel):
    name: Optional[str] = Field(None, description="Nombre PDV")


# Models for Sucursal API -----------------
class SucursalModel(BaseModel):
    name: str = Field(..., description="Nombre Sucursal")

    clients: List["ClientModel"] = Relationship(
        back_populates="sucursal",
        sa_relationship_kwargs={"description": "Lista de Clients en esta Sucursal"}
    )


# Canal Distribucion model -----------------
class CanalDistribucionModel(BaseModel):
    name: str = Field(..., description="Nombre Canal Distribucion")
    clients: List["ClientModel"] = Relationship(
        back_populates="canal_distribucion",
        sa_relationship_kwargs={"description": "Lista de Clients en este Canal Distribucion"}
    )


# Categoria Model -----------------
class CategoriaModel(BaseModel):
    name: str = Field(..., description="Nombre Categoria")
    clients: List["ClientModel"] = Relationship(
        back_populates="categoria",
        sa_relationship_kwargs={"description": "Lista de Clients en esta Categoria"}
    )


# Subcanal Adicional Model -----------------
class SubcanalAdicionalModel(BaseModel):
    name: str = Field(..., description="Nombre Subcanal Adicional")
    clients: List["ClientModel"] = Relationship(
        back_populates="subcanal_adicional",
        sa_relationship_kwargs={"description": "Lista de Clients en este Subcanal Adicional"}
    )


# Vendedor Model -----------------
class VendedorModel(BaseModel):
    name: str = Field(..., description="Nombre Vendedor")
    clients: List["ClientModel"] = Relationship(
        back_populates="vendedor",
        sa_relationship_kwargs={"description": "Lista de Clients en este Vendedor"}
    )


# Gerente Regional Model -----------------
class GerenteRegionalModel(BaseModel):
    name: str = Field(..., description="Nombre Gerente Regional")
    clients: List["ClientModel"] = Relationship(
        back_populates="gerente_regional",
        sa_relationship_kwargs={"description": "Lista de Clients en este Gerente Regional"}
    )


# Gerente Nacional Model -----------------
class GerenteNacionalModel(BaseModel):
    name: str = Field(..., description="Nombre Gerente Nacional")
    clients: List["ClientModel"] = Relationship(
        back_populates="gerente_nacional",
        sa_relationship_kwargs={"description": "Lista de Clients en este Gerente Nacional"}
    )


# Client model -----------------
class ClientModel(BaseModel):
    name: str = Field(..., description="Nombre Cliente")
    sucursal_id: Optional[int] = Field(
        default=None,
        foreign_key="sucursalmodel.id",
        description="Foreign key a SucursalModel"
    )
    canal_distribucion_id: Optional[int] = Field(
        default=None,
        foreign_key="canaldistribucionmodel.id",
        description="Foreign key a CanalDistribucionModel"
    )
    categoria_id: Optional[int] = Field(
        default=None,
        foreign_key="categorialmodel.id",
        description="Foreign key a CategoriaModel"
    )
    subcanal_adicional_id: Optional[int] = Field(
        default=None,
        foreign_key="subcanaladicionalmodel.id",
        description="Foreign key a SubcanalAdicionalModel"
    )
    vendedor_id: Optional[int] = Field(
        default=None,
        foreign_key="vendedormodel.id",
        description="Foreign key a VendedorModel"
    )
    gerente_regional_id: Optional[int] = Field(
        default=None,
        foreign_key="gerenteregionalmodel.id",
        description="Foreign key a GerenteRegionalModel"
    )
    gerente_nacional_id: Optional[int] = Field(
        default=None,
        foreign_key="gerentenacionalmodel.id",
        description="Foreign key a GerenteNacionalModel"
    )


# POIS Model -----------------
class POISTypeModel(BaseModel):
    name: str = Field(..., description="Nombre POI")
    pois: List["POIModel"] = Relationship(
        back_populates="pois_type",
        sa_relationship_kwargs={"description": "Lista de POIs en este tipo de POI"}
    )


class POIModel(BaseModel):
    name: str = Field(..., description="Nombre POI")
    pois_type_id: Optional[int] = Field(
        default=None,
        foreign_key="poistypemodel.id",
        description="Foreign key a POISTypeModel"
    )
    pdv_id: Optional[int] = Field(
        default=None,
        foreign_key="pdvmodel.id",
        description="Foreign key a PDVModel"
    )
