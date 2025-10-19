from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd
from sqlalchemy import Table
from sqlalchemy.engine import Engine

from .schema import build_metadata, import_order


SHEET_NAME_ALIASES: Dict[str, str] = {
    "clase": "clase",
    "clases": "clase",
    "linea": "linea",
    "lineas": "linea",
    "equipo": "equipo",
    "equipos": "equipo",
    "ot": "ot",
    "ots": "ot",
    "ordenestrabajo": "ot",
    "ordenes_trabajo": "ot",
    "reserva": "reserva",
    "reservas": "reserva",
    "material": "material",
    "materiales": "material",
    "reserva_material": "reserva_material",
    "reserva material": "reserva_material",
    "reserva_materiales": "reserva_material",
    "demora": "demora",
    "demoras": "demora",
    "produccion": "produccion",
    "producción": "produccion",
}

DATE_COLUMNS: Dict[str, Iterable[str]] = {
    "reserva": ("fecha",),
    "ot": ("fechaProg", "fechaRealiz"),
    "demora": ("fecha",),
    "produccion": ("fecha",),
}


class ExcelImporter:
    """Import data from an Excel workbook into a PostgreSQL database."""

    def __init__(self, engine: Engine, schema: str | None = None) -> None:
        self.engine = engine
        self.schema = schema
        self.metadata, self.tables = build_metadata(schema=schema)

    def load_workbook(self, path: Path) -> Dict[str, pd.DataFrame]:
        """Load all sheets from the Excel workbook."""

        if not path.exists():
            raise FileNotFoundError(f"Excel file not found: {path}")

        workbook = pd.read_excel(path, sheet_name=None)
        normalized = {}
        for raw_sheet_name, df in workbook.items():
            key = self._resolve_sheet_name(raw_sheet_name)
            if key and not df.empty:
                normalized[key] = self._clean_dataframe(key, df)
        return normalized

    def import_data(
        self,
        path: Path,
        *,
        create_tables: bool = False,
        truncate_before_load: bool = False,
    ) -> None:
        """Import workbook data into the database."""

        sheet_data = self.load_workbook(path)

        if create_tables:
            self.metadata.create_all(self.engine)

        with self.engine.begin() as connection:
            if truncate_before_load:
                for table in reversed(list(import_order(self.tables))):
                    connection.execute(table.delete())

            for table in import_order(self.tables):
                df = sheet_data.get(table.name)
                if df is None or df.empty:
                    continue

                records: List[dict] = df.to_dict(orient="records")
                if not records:
                    continue

                connection.execute(table.insert(), records)

    def _resolve_sheet_name(self, sheet_name: str) -> str | None:
        key = sheet_name.strip().lower().replace(" ", "_")
        return SHEET_NAME_ALIASES.get(key)

    def _clean_dataframe(self, table_key: str, df: pd.DataFrame) -> pd.DataFrame:
        df = df.rename(columns=lambda c: c.strip())
        df = df.where(pd.notnull(df), None)

        date_columns = DATE_COLUMNS.get(table_key, ())
        for column in date_columns:
            if column in df.columns:
                df[column] = pd.to_datetime(df[column], errors="coerce")

        return df


__all__ = ["ExcelImporter"]
