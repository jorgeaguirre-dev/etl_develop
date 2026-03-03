import os
from dagster import sensor, RunRequest, AssetKey, AssetSelection

#from my_etl.assets.staging_assets import stg_cablemodems, stg_clientes
#from my_etl.assets.business_assets import reporte_final

@sensor(
    name="sensor_actualizacion_json",
    minimum_interval_seconds=60, # Revisa cada 1 minuto
    target=AssetSelection.all()
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
                asset_selection=[
                    AssetKey("stg_cablemodems"),
                    AssetKey("stg_clientes"),
                    AssetKey("reporte_final")
                ]
            )