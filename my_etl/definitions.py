from dagster import Definitions, load_assets_from_modules
# Importación absoluta basada en la raíz del proyecto
import my_etl.assets.raw_assets as raw_assets
import my_etl.assets.staging_assets as staging_assets
import my_etl.assets.business_assets as business_assets

all_assets = load_assets_from_modules([raw_assets, staging_assets, business_assets])

defs = Definitions(
    assets=all_assets,
)
