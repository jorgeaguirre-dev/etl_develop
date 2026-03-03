from dagster import asset, AssetIn
import pandas as pd
from datetime import datetime

@asset(
    group_name="business",
    ins={
        "clientes": AssetIn("stg_clientes"),
        "modems": AssetIn("stg_cablemodems")
    }
)
def reporte_final(clientes, modems):
    """Genera el reporte final con lógica de estado_cm."""
    # Join 1:N
    df = pd.merge(modems, clientes, on="id_cliente", how="inner")

    # Lógica de enumerado estado_cm
    def definir_estado(row):
        return "Correcto" if row['power'] > 0 and row['delay'] < 4 else "Incorrecto"

    df['estado_cm'] = df.apply(definir_estado, axis=1)

    # Selección de columnas requeridas
    reporte = df[['nombre_completo', 'mac', 'nodo', 'power', 'delay', 'estado_cm']]

    # Persistencia para reconstrucción (Datalake Warehouse)
    # Guardamos con fecha para el histórico y uno fijo para el reporte actual
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M")
    reporte.to_csv(f"data/business/reporte_{fecha_str}.csv", index=False)
    reporte.to_csv("data/business/reporte_actual.csv", index=False)
    
    return reporte