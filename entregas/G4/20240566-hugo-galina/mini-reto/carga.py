import csv
import subprocess
import os

DATA_DIR = os.path.join("data", "mini-reto", "G4-iot")
SENSORES_CSV = os.path.join(DATA_DIR, "sensores.csv")
LECTURAS_CSV = os.path.join(DATA_DIR, "lecturas.csv")
ALERTAS_CSV = os.path.join(DATA_DIR, "alertas.csv")

sensor_info = {} # Mapea sensor_id -> {'sitio_id': ..., 'tipo': ...}

statements = ["USE iot_20240566;"]

# 1. Cargar c1_ficha_sensor y mapear la metadata de sensores
if os.path.exists(SENSORES_CSV):
    with open(SENSORES_CSV, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s_id = row.get('sensor_id') or row.get('id_sensor')
            st_id = row.get('sitio_id') or row.get('id_sitio')
            tipo = row.get('tipo', '')
            inst = row.get('instalado_en', '')
            
            sensor_info[s_id] = {'sitio_id': st_id, 'tipo': tipo}
            
            stmt = f"INSERT INTO c1_ficha_sensor (sensor_id, sitio_id, tipo, instalado_en) VALUES ('{s_id}', '{st_id}', '{tipo}', '{inst}');"
            statements.append(stmt)

# 2. Cargar c2_c4_lecturas_sensor
if os.path.exists(LECTURAS_CSV):
    with open(LECTURAS_CSV, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            s_id = row.get('sensor_id') or row.get('id_sensor')
            leida = row.get('leida_en') or row.get('fecha')
            val = float(row.get('valor', 0.0))
            
            stmt = f"INSERT INTO c2_c4_lecturas_sensor (sensor_id, leida_en, valor) VALUES ('{s_id}', '{leida}', {val});"
            statements.append(stmt)

# 3. Cargar c3_alertas_sitio desnormalizado
if os.path.exists(ALERTAS_CSV):
    with open(ALERTAS_CSV, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            a_id = row.get('alerta_id') or row.get('id_alerta')
            s_id = row.get('sensor_id') or row.get('id_sensor')
            
            # Si sitio_id no viene en alertas.csv, se busca del sensor correspondiente
            st_id = row.get('sitio_id') or row.get('id_sitio') or sensor_info.get(s_id, {}).get('sitio_id', '')
            gen = row.get('generada_en') or row.get('fecha')
            niv = row.get('nivel', '')
            msg = row.get('mensaje', '').replace("'", "''")
            tipo = sensor_info.get(s_id, {}).get('tipo', 'Desconocido')
            
            stmt = f"INSERT INTO c3_alertas_sitio (sitio_id, generada_en, alerta_id, sensor_id, tipo, nivel, mensaje) VALUES ('{st_id}', '{gen}', '{a_id}', '{s_id}', '{tipo}', '{niv}', '{msg}');"
            statements.append(stmt)

# Guardar un archivo cql temporal para evitar saturar el buffer
script_path = os.path.join("entregas", "G4", "20240566-hugo-galina", "mini-reto", "temp_carga.cql")
with open(script_path, "w", encoding="utf-8") as f:
    f.write("\n".join(statements))

print("Archivo de carga CQL generado. Insertando datos en Cassandra...")

cmd = f"docker exec -i cassandra3 cqlsh --request-timeout=60 < {script_path}"
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)

if os.path.exists(script_path):
    os.remove(script_path)

if res.returncode == 0:
    print("¡Carga masiva completada con éxito!")
else:
    print("Error durante la carga:", res.stderr)