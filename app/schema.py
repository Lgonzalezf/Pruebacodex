from __future__ import annotations

from typing import Dict, Iterable, Tuple

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
)


def build_metadata(schema: str | None = None) -> Tuple[MetaData, Dict[str, Table]]:
    """Create SQLAlchemy metadata and table objects for the domain."""

    metadata = MetaData(schema=schema)

    clase = Table(
        "clase",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("descripcion", String(255), nullable=False),
    )

    linea = Table(
        "linea",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("descripcion", String(255), nullable=False),
    )

    equipo = Table(
        "equipo",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("codigo", String(50), nullable=False, unique=True),
        Column("nombre", String(255), nullable=False),
        Column("marca", String(255)),
        Column("modelo", String(255)),
        Column("claseId", ForeignKey(clase.c.id), nullable=False),
        Column("lineaId", ForeignKey(linea.c.id), nullable=False),
    )

    reserva = Table(
        "reserva",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("fecha", Date, nullable=False),
    )

    material = Table(
        "material",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("descripcion", String(255), nullable=False),
        Column("fabricante", String(255)),
        Column("nParte", String(255)),
        Column("unidad", String(50)),
    )

    reserva_material = Table(
        "reserva_material",
        metadata,
        Column("reservaId", ForeignKey(reserva.c.id), primary_key=True),
        Column("materialId", ForeignKey(material.c.id), primary_key=True),
        Column("cantidad", Numeric(asdecimal=False), nullable=True),
    )

    ot = Table(
        "ot",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("descripcion", String(255), nullable=False),
        Column("tipo", String(100), nullable=False),
        Column("fechaProg", DateTime, nullable=True),
        Column("fechaRealiz", DateTime, nullable=True),
        Column("estado", String(50), nullable=False),
        Column("equipoId", ForeignKey(equipo.c.id), nullable=False),
        Column("reservaId", ForeignKey(reserva.c.id), nullable=False, unique=True),
    )

    demora = Table(
        "demora",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("codigo", String(50), nullable=False, unique=True),
        Column("responsable", String(255), nullable=False),
        Column("tiempo", Float, nullable=False),
        Column("fecha", DateTime, nullable=False),
        Column("lineaId", ForeignKey(linea.c.id), nullable=False),
    )

    produccion = Table(
        "produccion",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("tonelajeProcesado", Float, nullable=False),
        Column("fecha", Date, nullable=False),
        Column("lineaId", ForeignKey(linea.c.id), nullable=False),
    )

    tables = {
        "clase": clase,
        "linea": linea,
        "equipo": equipo,
        "reserva": reserva,
        "material": material,
        "reserva_material": reserva_material,
        "ot": ot,
        "demora": demora,
        "produccion": produccion,
    }

    return metadata, tables


def import_order(table_mapping: Dict[str, Table]) -> Iterable[Table]:
    """Return the tables in an order that satisfies foreign key constraints."""

    table_names = [
        "clase",
        "linea",
        "equipo",
        "material",
        "reserva",
        "reserva_material",
        "ot",
        "demora",
        "produccion",
    ]
    return [table_mapping[name] for name in table_names]


__all__ = ["build_metadata", "import_order"]
