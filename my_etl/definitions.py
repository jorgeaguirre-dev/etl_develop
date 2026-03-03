from dagster import Definitions, load_assets_from_modules
# Importación absoluta basada en la raíz del proyecto
import my_etl.assets.staging_assets as staging_assets
import my_etl.assets.business_assets as business_assets
from my_etl.sensors.file_sensors import cablemodem_json_sensor

all_assets = load_assets_from_modules([staging_assets, business_assets])

defs = Definitions(
    assets=all_assets,
    sensors=[cablemodem_json_sensor],
)
