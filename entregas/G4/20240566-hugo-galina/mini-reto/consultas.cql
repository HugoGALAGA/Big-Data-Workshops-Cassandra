USE iot_20240566;

-- C1. Ficha de un sensor
SELECT sensor_id, sitio_id, tipo, instalado_en
FROM c1_ficha_sensor
WHERE sensor_id = 'se005';

-- C2. La lectura más reciente de un sensor
SELECT leida_en, valor
FROM c2_lectura_reciente
WHERE sensor_id = 'se042'
LIMIT 1;

-- C3. Las 10 alertas más recientes de un sitio, con el tipo de sensor
SELECT generada_en, sensor_id, tipo, nivel, mensaje
FROM c3_alertas_sitio
WHERE sitio_id = 'si08'
LIMIT 10;

-- C4. Cuántas lecturas tuvo un sensor entre las 08:00 y las 11:59 de un día, y el valor máximo
SELECT COUNT(*) AS lecturas, MAX(valor) AS maximo
FROM c4_metricas_sensor
WHERE sensor_id = 'se042'
  AND leida_en >= '2026-09-25 08:00:00+0000' AND leida_en < '2026-09-25 12:00:00+0000';