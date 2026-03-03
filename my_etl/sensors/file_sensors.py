import os
from dagster import sensor, RunRequest, DefaultSensorStatus, SensorDefinition, AssetSelection

@sensor(
    name="sensor_nuevo_json",
    target=AssetSelection.groups("staging", "business"),
    minimum_interval_seconds=60 # Chequea cada minuto si hubo cambios
)
def cablemodem_file_sensor(context):
    path = "data/raw/cablemodems/cablemodems.json"
    if os.path.exists(path):
        # Obtenemos la fecha de última modificación
        mtime = os.path.getmtime(path)
        # El cursor guarda el último mtime que procesamos
        last_mtime = context.cursor
        
        if last_mtime is None or float(mtime) > float(last_mtime):
            context.update_cursor(str(mtime))
            yield RunRequest(
                run_key=f"update_{mtime}",
                message="Se detectó una actualización en el JSON de cablemodems."
            )