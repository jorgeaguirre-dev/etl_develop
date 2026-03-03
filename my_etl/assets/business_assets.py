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
    """Genera el reporte final: (nombre_completo, mac, nodo, power, delay, estado_cm)"""
    
    # Join (N modems : 1 cliente)
    df = pd.merge(modems, clientes, on="id_cliente", how="inner")

    # Lógica del enumerado estado_cm
    # Correcto: power > 0 y delay < 4 | Incorrecto: Caso contrario
    def calcular_estado_cm(row):
        if row['power'] > 0 and row['delay'] < 4:
            return "Correcto"
        return "Incorrecto"

    df['estado_cm'] = df.apply(calcular_estado_cm, axis=1)

    # Selección de columnas finales según formato pedido
    reporte = df[[
        'nombre_completo',
        'mac',
        'nodo',
        'power',
        'delay',
        'estado_cm'
    ]]

    # Persistencia en Datawarehouse local
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    reporte.to_csv(f"data/business/reporte_{timestamp}.csv", index=False)
    reporte.to_csv("data/business/reporte_actual.csv", index=False)
    
    return reporte