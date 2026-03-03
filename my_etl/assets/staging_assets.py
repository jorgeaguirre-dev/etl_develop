from dagster import asset
import pandas as pd
import json

@asset(group_name="staging")
def stg_clientes():
    """Carga y filtra solo clientes activos."""
    df = pd.read_csv("data/raw/clientes/clientes.csv")
    return df[df['estado'] == 'activo'].copy()

@asset(group_name="staging")
def stg_cablemodems():
    """Flatten del JSON y redondeo de power."""
    with open("data/raw/cablemodems/cablemodems.json", "r") as f:
        data = json.load(f)
    
    # Suponiendo que el JSON es una lista de objetos con 'modems' anidado
    df = pd.json_normalize(data, record_path=['modems'], meta=['id_cliente'])
    
    # Redondeo a 3 decimales según requerimiento
    df['power'] = df['power'].astype(float).round(3)
    
    # Solo cablemodems encendidos
    return df[df['online'] == True].copy()