# ETL Development

This project implements a data pipeline using Dagster for two purposes: as an orchestrator and as a data catalog. The ETL process ingests raw data from two data files that are updated with some frequency.
The transformation process is carried out through a staging layer, where data is cleaned and transformed, and then a final report is produced with the analysis of the cablemodem status.

## Main Features
- ✅ Automatic data ingestion
- ✅ Multi-layer data transformation
- ✅ Triggered by auto-detection of changes in raw files
- ✅ Historical report versioning
- ✅ Asset-based data architecture

## Business Logic

### Cablemodem Status Rules
The system evaluates the health of cablemodems based on:
- **Power Level**: Must be `greater than 0`
- **Delay**: Must be less than `4 milliseconds`

Modems that meet both requirements are classified as **"Correcto"**, otherwise they will be **"Incorrecto"**.

### Data Quality
- Only active clients are included in the report
- Only cablemodems in `On` state are processed
- Power measurement is rounded to `3 decimal places`
- All reports are marked with a `timestamp` for possible auditing

## Architecture
![Architecture](<img/Arquitectura ETL.drawio.png>)

## Data Pipeline
```
Raw Data → Staging Layer → Business Layer (BI)
```
The materialized Assets are observed shaping the Pipeline.

![DAG](img/DAG.png)

1. **Raw Layer** (`data/raw/`)
   - `clientes/clientes.csv` - Client information
   - `cablemodems/cablemodems.json` - Cablemodem telemetry data

2. **Staging Layer** (`data/staging/`)
   - `stg_clientes` - Filtered active clients with their name
   - `stg_cablemodems` - Filtered and flattened cablemodem data

3. **Business Layer** (`data/business/`)
   - `reporte_final` - Final report with cablemodem status analysis

### Staging Assets
The successful materialization of the assets is observed each time it occurs.
![Assets](img/Assets.png)

Here is a detailed description of what happens in each part of the pipeline and at which processing stage it occurs.

#### stg_clientes
- Loads client data from CSV
- Filters only active clients (`estado == True`)
- Creates the `nombre_completo` field (First name + Last name)
- Returns: `id_cliente`, `nombre_completo`

#### stg_cablemodems
- Loads cablemodem data from JSON
- Flattens the JSON structure
- Inherits `nodo` and `id_cliente` from the top level
- Rounds `power` to 3 decimal places
- Filters only powered-on modems (`encendido == True`)
- Returns: `id_cliente`, `mac`, `nodo`, `power`, `delay`

### Business Assets
The final report is generated here.
#### reporte_final
- Performs a join between clients and cablemodems (1:N)
- Calculates `estado_cm` (cablemodem status):
  - **Correcto**: `power > 0` and `delay < 4`
  - **Incorrecto**: Any other case
- Generates report with timestamp
- Outputs:
  - `reporte_{timestamp}.csv` - Historical snapshot
  - `reporte_actual.csv` - Latest version

**Report Columns:**
- `nombre_completo` - Client full name
- `mac` - Cablemodem MAC address
- `nodo` - Network node
- `power` - Signal power level
- `delay` - Delay
- `estado_cm` - Modem status (Correcto/Incorrecto)

![Current Report](img/reporte_actual.png)

## Automation
Pipeline automation is based on the use of a sensor that monitors changes in the raw data files. This sensor checks every minute for any changes and triggers updates and recalculation based on the new data. The process also generates a new versioned report for historical tracking.

- Checks every 60 seconds
- Detects file modifications using the timestamp
- Automatically triggers the full pipeline when a change is detected
- Runs: `stg_cablemodems` → `stg_clientes` → `reporte_final`

![Automation](img/automation.png)

### Raw Files Sensor
The ticks where the monitoring (check) of the raw stage files occurs are visible.
The `cablemodem_json_sensor` sensor monitors changes in the cablemodem JSON file.

![Sensor Tick](img/sensor_tick.png)

Below, the log stream generated when changes are detected in the `.json` file is shown, produced as part of the functional testing.

![Log Autorun](img/log_autorun.png)

## Installation

### Prerequisites
- Python 3.8+
- pip

### Dependencies
- **pandas** - Data manipulation and analysis
- **dagster** - Orchestration
- **dagster-webserver** - Web UI for monitoring

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set Dagster Home
export DAGSTER_HOME=$(pwd)/.dagster_home
```

## Starting and Accessing Dagster

```bash
export DAGSTER_HOME=$(pwd)/.dagster_home
dagster dev -f my_etl/definitions.py
```
### UI Access
To access the UI from a browser go to: http://localhost:3000

![Autorun](img/autorun.png)

## Future Improvements
- [ ] Add data validation checks
- [ ] Implement error handling and alerts
- [ ] Add support for multiple data sources
- [ ] Create analytical dashboards
- [ ] Implement incremental processing for large datasets