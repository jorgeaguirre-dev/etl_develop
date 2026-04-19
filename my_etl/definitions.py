from dagster import Definitions, load_assets_from_modules
# Absolute import based on the project root
import my_etl.assets.staging_assets as staging_assets
import my_etl.assets.business_assets as business_assets
from my_etl.sensors.file_sensors import cablemodem_json_sensor

all_assets = load_assets_from_modules([staging_assets, business_assets])

defs = Definitions(
    assets=all_assets,
    sensors=[cablemodem_json_sensor],
)
