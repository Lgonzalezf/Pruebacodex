from __future__ import annotations

import argparse
from pathlib import Path

from .config import Settings
from .database import get_engine
from .excel_importer import ExcelImporter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Carga datos desde un archivo Excel a una base de datos Neon/PostgreSQL.",
    )
    parser.add_argument("excel_path", help="Ruta al archivo de Excel con los datos.")
    parser.add_argument(
        "--create-tables",
        action="store_true",
        help="Crear las tablas en la base de datos antes de cargar los datos.",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Vaciar las tablas antes de cargar nuevos datos.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    settings = Settings.load()
    engine = get_engine(settings.database_url)
    importer = ExcelImporter(engine, schema=settings.schema)

    importer.import_data(
        Path(args.excel_path),
        create_tables=args.create_tables,
        truncate_before_load=args.truncate,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
