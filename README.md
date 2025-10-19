# Cargador de datos a Neon desde Excel

Esta aplicación en Python permite crear las tablas necesarias y cargar datos a una base de datos [Neon](https://neon.tech/) (PostgreSQL administrado) a partir de un libro de Excel. El libro debe contener una hoja por cada entidad del modelo de mantenimiento industrial descrito a continuación.

## Requisitos previos

1. Tener instalado Python 3.11 o superior.
2. Contar con un entorno virtual (recomendado).
3. Disponer de una base de datos Neon/PostgreSQL y de la cadena de conexión correspondiente.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows usar: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Copia el archivo `.env.example` a `.env` y actualiza la variable `DATABASE_URL` con la cadena de conexión completa. Opcionalmente puedes definir `DATABASE_SCHEMA` si quieres crear las tablas en un esquema distinto de `public`.

```bash
cp .env.example .env
```

El valor esperado para `DATABASE_URL` tiene el siguiente formato:

```
postgresql+psycopg2://usuario:password@host:puerto/base_de_datos
```

## Estructura del libro de Excel

Cada hoja debe contener las columnas indicadas en las tablas siguientes. Los nombres de las hojas pueden estar en singular o plural (por ejemplo `Clase` o `Clases`).

| Hoja | Columnas requeridas |
|------|---------------------|
| `Clase` | `id`, `descripcion` |
| `Linea` | `id`, `descripcion` |
| `Equipo` | `id`, `codigo`, `nombre`, `marca`, `modelo`, `claseId`, `lineaId` |
| `Material` | `id`, `descripcion`, `fabricante`, `nParte`, `unidad` |
| `Reserva` | `id`, `fecha` |
| `Reserva_Material` | `reservaId`, `materialId`, `cantidad` (opcional) |
| `OT` | `id`, `descripcion`, `tipo`, `fechaProg`, `fechaRealiz`, `estado`, `equipoId`, `reservaId` |
| `Demora` | `id`, `codigo`, `responsable`, `tiempo`, `fecha`, `lineaId` |
| `Produccion` | `id`, `tonelajeProcesado`, `fecha`, `lineaId` |

Los campos de fecha admiten formatos reconocidos por Excel; la aplicación se encarga de convertirlos a los tipos de datos adecuados en la base de datos.

## Uso

Ejecuta el comando principal indicando la ruta al archivo de Excel:

```bash
python -m app.main datos.xlsx
```

Opciones disponibles:

- `--create-tables`: crea las tablas en la base de datos antes de cargar la información.
- `--truncate`: elimina el contenido existente de las tablas antes de la carga.

Ejemplo completo:

```bash
python -m app.main datos.xlsx --create-tables --truncate
```

## Tablas creadas

La aplicación genera las siguientes tablas (con llaves foráneas incluidas):

1. `clase` — tipos o categorías de equipos.
2. `linea` — agrupa equipos, demoras y producción.
3. `equipo` — activos o máquinas.
4. `material` — insumos o repuestos.
5. `reserva` — agrupa los materiales usados en una OT.
6. `reserva_material` — tabla intermedia para la relación N:N entre reservas y materiales.
7. `ot` — órdenes de trabajo asociadas a un equipo y una reserva.
8. `demora` — registro de paradas en la línea.
9. `produccion` — registro de tonelaje procesado por línea.

## Desarrollo

El código fuente principal se encuentra en el paquete `app/`:

- `config.py`: carga de variables de entorno.
- `database.py`: creación de la conexión con SQLAlchemy.
- `schema.py`: definición de las tablas y relaciones.
- `excel_importer.py`: carga y normalización del libro de Excel.
- `main.py`: interfaz de línea de comandos.

Se puede extender el proyecto para manejar validaciones adicionales o registrar logs de auditoría según sea necesario.
