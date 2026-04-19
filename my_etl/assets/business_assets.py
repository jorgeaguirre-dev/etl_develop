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
    """Generates the final report: (nombre_completo, mac, nodo, power, delay, estado_cm)"""
    
    # Join (N modems : 1 client)
    df = pd.merge(modems, clientes, on="id_cliente", how="inner")

    # estado_cm logic
    # Correcto: power > 0 and delay < 4 | Incorrecto: any other case
    def calcular_estado_cm(row):
        if row['power'] > 0 and row['delay'] < 4:
            return "Correcto"
        return "Incorrecto"

    df['estado_cm'] = df.apply(calcular_estado_cm, axis=1)

    # Select final columns in the required report format
    reporte = df[[
        'nombre_completo',
        'mac',
        'nodo',
        'power',
        'delay',
        'estado_cm'
    ]]

    # Persist to local data warehouse
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    reporte.to_csv(f"data/business/reporte_{timestamp}.csv", index=False)
    reporte.to_csv("data/business/reporte_actual.csv", index=False)
    
    return reporte
