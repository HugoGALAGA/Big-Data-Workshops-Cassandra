CREATE KEYSPACE IF NOT EXISTS iot_20240566
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'dc-g4': 3
};

USE iot_20240566;

-- Tabla 1 (para C1): Ficha de un sensor
CREATE TABLE IF NOT EXISTS c1_ficha_sensor (
    sensor_id text,
    sitio_id text,
    tipo text,
    instalado_en timestamp,
    PRIMARY KEY (sensor_id)
);

-- Tabla 2 (para C2): La lectura más reciente de un sensor
CREATE TABLE IF NOT EXISTS c2_lectura_reciente (
    sensor_id text,
    leida_en timestamp,
    valor double,
    PRIMARY KEY (sensor_id, leida_en)
) WITH CLUSTERING ORDER BY (leida_en DESC);

-- Tabla 3 (para C3): Alertas por sitio con tipo de sensor desnormalizado
CREATE TABLE IF NOT EXISTS c3_alertas_sitio (
    sitio_id text,
    generada_en timestamp,
    alerta_id text,
    sensor_id text,
    tipo text,
    nivel text,
    mensaje text,
    PRIMARY KEY (sitio_id, generada_en, alerta_id)
) WITH CLUSTERING ORDER BY (generada_en DESC, alerta_id ASC);

-- Tabla 4 (para C4): Lecturas de un sensor para métricas y aggregations por rango
CREATE TABLE IF NOT EXISTS c4_metricas_sensor (
    sensor_id text,
    leida_en timestamp,
    valor double,
    PRIMARY KEY (sensor_id, leida_en)
) WITH CLUSTERING ORDER BY (leida_en DESC);