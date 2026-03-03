import os
from dagster import sensor, RunRequest, AssetSelection, SensorDefinition

@sensor(
    name="sensor_actualizacion_json",
    minimum_interval_seconds=300, # Revisa cada 5 minutos
)
def cablemodem_json_sensor(context):
    file_path = "data/raw/cablemodems/cablemodems.json"
    
    if os.path.exists(file_path):
        mtime = os.path.getmtime(file_path)
        # Recuperamos el último tiempo procesadoo del cursor
        last_mtime = context.cursor
        
        # Si es la primera vez o si el archivo es más nuevo que el anterior
        if last_mtime is None or float(mtime) > float(last_mtime):
            # Guardamos el nuevo timestamp
            context.update_cursor(str(mtime))
            yield RunRequest(
                run_key=f"json_updated_{mtime}",
                message="Se detectó una nueva versión del archivo de cablemódems.",
                # Ejecuta todo el flujo
                asset_selection=AssetSelection.all()
            )