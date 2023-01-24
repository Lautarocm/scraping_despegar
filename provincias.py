import json
import requests

provincias = []

# tomar datos de provincias
provincias_json = requests.get("https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.2/download/provincias.json").content
obj_provincias = json.loads(provincias_json)["provincias"]

for provincia in obj_provincias:
    provincias.append(provincia["nombre"])