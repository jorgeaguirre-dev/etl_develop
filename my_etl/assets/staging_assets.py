import pandas as pd
import json
from dagster import asset

@asset(group_name="staging")
def stg_clientes():
    """Loads clients, filters active ones and generates nombre_completo."""
    df = pd.read_csv("data/raw/clientes/clientes.csv")
    # Filter by the 'estado' field (True)
    df = df[df['estado'] == True].copy()
    
    # Create nombre_completo in the required format
    df['nombre_completo'] = df['nombre'] + " " + df['apellido']
    
    # Ensure correct data type for the join
    df['id_cliente'] = df['id_cliente'].astype(int)
    
    return df[['id_cliente', 'nombre_completo']]

@asset(group_name="staging")
def stg_cablemodems():
    """Flattens the JSON, inherits 'nodo' and filters by 'encendido'."""
    with open("data/raw/cablemodems/cablemodems.json", "r") as f:
        data = json.load(f)
    
    # 'nodo' and 'id_cliente' are at the root level of the JSON object
    df = pd.json_normalize(
        data,
        record_path=['cablemodems'],
        meta=['id_cliente', 'nodo']
    )
    
    # Requirement: Round power to 3 decimal places
    df['power'] = df['power'].astype(float).round(3)
    
    # Filter: Only powered-on cablemodems
    df = df[df['encendido'] == True].copy()
    
    # Ensure correct data type for the join
    df['id_cliente'] = df['id_cliente'].astype(int)
    
    return df
