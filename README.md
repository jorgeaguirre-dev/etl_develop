# 4 - Desarrollo ETL



## Dagster
Usado no solo como orquestador sinó también como catálogo de datos vivo donde el estado de cada reporte es rastreable.

```bash
export DAGSTER_HOME=/home/repo/Challenges/4_desarrollo_etl/.dagster_home
dagster dev -f my_etl/definitions.py

export DAGSTER_HOME=$(pwd)/.dagster_home
dagster dev -f my_etl/definitions.py -h 0.0.0.0 -p 3000

export DAGSTER_HOME=$(pwd)/.dagster_home
PYTHONPATH=. venv/bin/dagster dev -m my_etl.definitions -h 0.0.0.0 -p 3000
```

http://localhost:3000

## Instalación
```bash
pip install -r requirements.txt
```


