from datetime import date, timedelta
from io import StringIO
import pandas as pd
import requests


def obtener_tabla(response):
    if response.status_code == 200:
        html = StringIO(response.text)
        tables = pd.read_html(html)
        return tables[0]
    else:
        print("Error:", response.status_code)
        return None


def check_weekend() -> bool:
    ayer = date.today() - timedelta(days=1)
    return ayer.isoweekday() == 7


# -------- INICIO DEL PROGRAMA --------

if check_weekend():
    ayer = date.today() - timedelta(days=2)
else:
    ayer = date.today() - timedelta(days=1)

url = "http://10.16.49.45:888/pvpap/uni_cont.php"

data1 = {
    "Fecha_Inicio": ayer.strftime("%m/%d/%Y"),
    "agente": "9"
}

data2 = {
    "Fecha_Inicio": ayer.strftime("%m/%d/%Y"),
    "agente": "10"
}

response1 = requests.post(url, data=data1)
response2 = requests.post(url, data=data2)

tabla1 = obtener_tabla(response1)
tabla2 = obtener_tabla(response2)

if tabla1 is not None and tabla2 is not None:
    ventas_totales = pd.concat([tabla1, tabla2], ignore_index=True)
    nombre_archivo = f"uniformes_{ayer}.xlsx"
    ventas_totales.to_excel(nombre_archivo, index=False)
    print("Excel generado correctamente.")