from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import DateTime, Field, Relationship, SQLModel


def get_utc_now():
    """ Get current UTC datetime.
    """
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)


"""
Columns:
* (ok) id_pdv_unique
* (ok) id_cli_suc_cuenta
* (ok) id_cod_pdv
* (ok) desc_cli_suc_cuenta
* (ok) id_tie_fecha_alta
* (ok) pv_x
* (ok) pv_y
* (ok) id_cli_canal_dist
* (ok) desc_cli_canal_dist
* (ok) id_cli_categoria_dist
* (ok) id_cli_subcanal_adic_dist
* (ok) desc_cli_subcanal_dist
* (ok) pv_pcia
* (ok) pv_departamento
* (ok) geohash
* (ok) id_cli_vendedor
* (ok) desc_cli_vendedor
* (ok) id_cli_gte_regional
* (ok) desc_cli_gte_regional
* (ok) id_cli_gte_nacional
* (ok) desc_cli_gte_nacional
* (ok) indicar_cantidad_de_bandejas
* (ok) indique_la_cantidad_de_m2_de_la_tienda
* (ok) indique_la_cantidad_de_pasillos
* (ok) indique_la_cantidad_de_puertas_de_heladeras
* (ok)
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
"""


class BaseModel(SQLModel):
    id: str = Field(
        primary_key=True,
        index=True,
        description="ID",
    )
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


class BaseModelAutoId(SQLModel):
    id: int = Field(
        primary_key=True,
        index=True,
        description="ID",
    )
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


# Client model -----------------
class Client(BaseModel, table=True):
    name: str = Field(..., description="Nombre Cliente")
    canales_distribucion: List["CanalDistribucion"] = Relationship(
        back_populates="client",
    )
    categorias: List["Categoria"] = Relationship(
        back_populates="client"
    )
    gerentes_regionales: List["GerenteRegional"] = Relationship(
        back_populates="client",
    )
    gerentes_nacionales: List["GerenteNacional"] = Relationship(
        back_populates="client",
    )
    pdvs: List["PDV"] = Relationship(
        back_populates="client",
    )
    subcanales_adicionales: List["SubcanalAdicional"] = Relationship(
        back_populates="client",
    )
    sucursales: List["Sucursal"] = Relationship(
        back_populates="client",
    )
    vendedores: List["Vendedor"] = Relationship(
        back_populates="client",
    )


# Departamentos Model -----------------
class Departamento(BaseModelAutoId, table=True):
    """ Model for Departamentos"""
    name: str = Field(..., description="Nombre Departamento")
    provincia_id: Optional[int] = Field(
        foreign_key="provincia.id",
    )
    provincia: Optional["Provincia"] = Relationship(
        back_populates="departamentos",
    )


# Provincias Model -----------------
class Provincia(BaseModelAutoId, table=True):
    """ Model for Provincias
    """
    name: str = Field(..., description="Nombre Provincia")
    departamentos: List["Departamento"] = Relationship(
        back_populates="provincia",
    )


# Models for PDV API -----------------
class PDV(BaseModel, table=True):
    cod_pdv: str = Field(..., description="Código PDV")
    fecha_alta: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        description="Fecha de alta",
        nullable=True,
    )
    lat: float = Field(..., description="PDV latitud")
    lon: float = Field(..., description="PDV longitud")
    pois: List["POI"] = Relationship(back_populates="pdv")
    geohash: str = Field(..., description="Geohash del PDV")
    bandejas: Optional[str] = Field(default=None, description="Número de bandejas")
    m2: Optional[str] = Field(default=None, description="Número de m2")
    pasillos: Optional[str] = Field(default=None, description="Número de pasillos")
    puertas_heladeras: Optional[str] = Field(
        default=None,
        description="Número de puertas de heladeras"
    )
    puntos_cobro: Optional[str] = Field(
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
    otros_servicios: Optional[bool] = Field(
        default=None,
        description="Cuenta con otros servicios (ej: tarjeta colectivos, carga celular, cospeles, rapipago, pago facil)"
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
    freezer: Optional[str] = Field(
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
    client_id: Optional[str] = Field(foreign_key="client.id")
    client: Optional["Client"] = Relationship(back_populates="pdvs")


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
        foreign_key="Departamento.id",
        description="Foreign key a Departamento"
    )
    geohash: str = Field(..., description="Geohash del PDV")


class PDVListSchema(SQLModel):
    results: List[PDV] = Field(..., description="Listas de PDVs")
    count: int = Field(..., description="Total de PDVs")


class UpdatePDVSchema(SQLModel):
    name: Optional[str] = Field(None, description="Nombre PDV")


# Models for Sucursal API -----------------
class Sucursal(BaseModel, table=True):
    name: str = Field(..., description="Nombre Sucursal")
    client_id: Optional[str] = Field(foreign_key="client.id")
    client: Optional["Client"] = Relationship(back_populates="sucursales")


# Canal Distribucion model -----------------
class CanalDistribucion(BaseModel, table=True):
    name: str = Field(..., description="Nombre Canal Distribucion")
    client_id: Optional[str] = Field(foreign_key="client.id")
    client: Optional["Client"] = Relationship(back_populates="canales_distribucion")


# Categoria Model -----------------
class Categoria(BaseModel, table=True):
    name: str = Field(..., description="Nombre Categoria")
    client_id: Optional[str] = Field(foreign_key="client.id")
    client: Optional["Client"] = Relationship(back_populates="categorias")


# Subcanal Adicional Model -----------------
class SubcanalAdicional(BaseModel, table=True):
    """ Model for Subcanal Adicional
    """
    name: str = Field(..., description="Nombre Subcanal Adicional")
    client_id: Optional[str] = Field(foreign_key="client.id")
    client: Optional["Client"] = Relationship(back_populates="subcanales_adicionales")


# Vendedor Model -----------------
class Vendedor(BaseModel, table=True):
    name: str = Field(..., description="Nombre Vendedor")
    client_id: Optional[str] = Field(foreign_key="client.id")
    client: Optional["Client"] = Relationship(back_populates="vendedores")


# Gerente Regional Model -----------------
class GerenteRegional(BaseModel, table=True):
    """ Model for Gerente Regional
    """
    name: str = Field(..., description="Nombre Gerente Regional")
    client_id: Optional[str] = Field(foreign_key="client.id")
    client: Optional["Client"] = Relationship(back_populates="gerentes_regionales")


# Gerente Nacional Model -----------------
class GerenteNacional(BaseModel, table=True):
    name: str = Field(..., description="Nombre Gerente Nacional")
    client_id: Optional[str] = Field(foreign_key="client.id")
    client: Optional["Client"] = Relationship(back_populates="gerentes_nacionales")


# POIS Model -----------------
class POISType(BaseModel, table=True):
    """ Model for POIS
    """
    name: str = Field(..., description="Nombre POI")
    pois: List["POI"] = Relationship(back_populates="pois_type")


class POI(BaseModel, table=True):
    """ Model for POI
    """
    name: str = Field(..., description="Nombre POI")
    pois_type_id: Optional[str] = Field(foreign_key="poistype.id")
    pois_type: Optional["POISType"] = Relationship(back_populates="pois")
    pdv_id: Optional[str] = Field(foreign_key="pdv.id")
    pdv: Optional["PDV"] = Relationship(back_populates="pois")
