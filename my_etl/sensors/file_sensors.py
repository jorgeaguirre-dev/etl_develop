import os
from dagster import sensor, RunRequest, AssetKey, AssetSelection

#from my_etl.assets.staging_assets import stg_cablemodems, stg_clientes
#from my_etl.assets.business_assets import reporte_final

@sensor(
    name="sensor_actualizacion_json",
    minimum_interval_seconds=60, # Checks every 1 minute
    target=AssetSelection.all()
)
def cablemodem_json_sensor(context):
    file_path = "data/raw/cablemodems/cablemodems.json"
    
    if os.path.exists(file_path):
        mtime = os.path.getmtime(file_path)
        # Retrieve the last processed timestamp from the cursor
        last_mtime = context.cursor
        
        # If it's the first run or the file is newer than the previous one
        if last_mtime is None or float(mtime) > float(last_mtime):
            # Save the new timestamp
            context.update_cursor(str(mtime))
            yield RunRequest(
                run_key=f"json_updated_{mtime}",
                message="A new version of the cablemodem file was detected.",
                # Run the full pipeline
                asset_selection=[
                    AssetKey("stg_cablemodems"),
                    AssetKey("stg_clientes"),
                    AssetKey("reporte_final")
                ]
            )
