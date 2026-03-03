# 4 - Desarrollo ETL

Este proyecto implementa un data pipeline usando Dagster para dos fines, como orquestador y catálogo de datos. El proceso ETL ingesta datos en bruto en dos archivos de datos que se actualizan con cierta frecuencia.
El proceso de transformación se realiza a través de una capa de staging, donde se limpian y transforman los datos, y luego se produce un reporte final con el análisis del estado de los cablemodems.

## Arquitectura

### Flujo de Datos
```
Datos en Bruto (Raw) → Capa Staging → Capa Business (BI)
```

1. **Capa Raw** (`data/raw/`)
   - `clientes/clientes.csv` - Información de Clientes
   - `cablemodems/cablemodems.json` - Datos de telemetría de Cable modems

2. **Capa Staging** (`data/staging/`)
   - `stg_clientes` - Clientes activos filtrados con su nombre
   - `stg_cablemodems` - Datos de cable modem filtrado y aplanado

3. **Business Layer** (`data/business/`)
   - `reporte_final` - Reporte Final con análisis de estado de cable modems

## Data Pipeline

### Assets de Staging

#### stg_clientes
- Carga datos de clientes desde CSV
- Filtra sólo clientes activos (`estado == True`)
- Se crea el campo `nombre_completo` (Nombre + Apellido)
- Devuelve: `id_cliente`, `nombre_completo`

#### stg_cablemodems
- Carga datos de cable modems desde JSON
- Aplana la estructura JSON
- Hereda `nodo` e `id_cliente` del nivel superior
- Redondea `power` a 3 decimales
- Filtra sólo modems encendidos (`encendido == True`)
- Devuelve: `id_cliente`, `mac`, `nodo`, `power`, `delay`

### Assets de Business

#### reporte_final
- Se realiza un join entre clientes y cablemodems (1:N)
- Calcula `estado_cm` (estado de cable modem):
  - **Correcto**: `power > 0` y `delay < 4`
  - **Incorrecto**: Otro caso
- Genera reporte con timestamp
- Outputs:
  - `reporte_{timestamp}.csv` - Snapshot histórica
  - `reporte_actual.csv` - ültima versión

**Columnas del Reporte:**
- `nombre_completo` - Nombre completo del cliente
- `mac` - MAC address del Cablemodem
- `nodo` - Nodo de Red
- `power` - Nivel de potencia de señal
- `delay` - Delay
- `estado_cm` - Estado del modem (Correcto/Incorrecto)

## Automatización

### Sensor de Archivos Raw
El sensor `cablemodem_json_sensor` monitorea cambios en el archivo JSON de cablemodems:
- Verifica cada 60 segundos
- Detecta modificaciones de archivo usando el timestamp
- Autimáticamente dispara el pipeline completo cuando el cambio es detectado
- Ejecuta: `stg_cablemodems` → `stg_clientes` → `reporte_final`

## Instalación

### Prerequisitos
- Python 3.8+
- pip

### Setup
```bash
# Instalar dependencias
pip install -r requirements.txt

# Setear el Home de Dagster
export DAGSTER_HOME=$(pwd)/.dagster_home
```

## Inicio y Consulta de Dagster

```bash
export DAGSTER_HOME=/home/repo/Challenges/4_desarrollo_etl/.dagster_home
dagster dev -f my_etl/definitions.py
```
### Acceso a la UI
Para acceder a la UI desde un navegador ir a: http://localhost:3000

