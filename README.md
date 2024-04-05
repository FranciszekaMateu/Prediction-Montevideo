# Proyecto de Recolección y Análisis de Datos

Este proyecto tiene como objetivo la recolección y análisis de datos provenientes de dos fuentes principales: una API pública proporcionada por la Intendencia de Montevideo para obtener datos de localizacion y velocidad de un omnibus, y otra API, Open Meteo, para obtener datos de temperatura y humedad. Estos datos se utilizarán para analizar su impacto en el transporte público, específicamente en la línea de ómnibus 117. 

## Descripción del Proceso

### Recolección de Datos
1. Se establecerá una conexión con la API pública de la Intendencia de Montevideo para obtener datos de temperatura.
2. Se conectará a la API Open Meteo para obtener datos de temperatura y humedad.
3. Se configurará un script para recolectar datos de temperatura,localizacion, velocidad,velocidad del viento y humedad cada 30 segundos durante un mes.
4. Los datos recopilados se almacenarán en una base de datos PostgreSQL utilizando Supabase.

### Análisis de Datos (Fase futura)
1. Los datos recopilados se limpiarán y prepararán para su análisis.
2. Se desarrollará un modelo de inteligencia artificial para predecir la velocidad, temperatura, humedad y ubicación actual del ómnibus en tiempo real.
3. Se implementará el modelo entrenado para realizar predicciones en tiempo real.

## Especificaciones Técnicas

- **Lenguaje de Programación:** Python
- **Base de Datos:** PostgreSQL
- **Plataforma de Desarrollo:** Supabase
- **Librerías Utilizadas:** 
    - Httpx: Para realizar solicitudes a las APIs.
    - supabase: Para la conexión y manipulación de la base de datos PostgreSQL.
    - pandas: Para la manipulación y análisis de datos (fase futura).
    - scikit-learn: Para el desarrollo del modelo de inteligencia artificial (fase futura).

## Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir al proyecto, no dudes en enviar un pull request.

## Notas Adicionales

- Este proyecto se basa en la premisa de que los datos de temperatura y humedad pueden afectar el transporte público.
- Se utiliza la API Open Meteo para obtener datos adicionales de humedad.
- La fase de entrenamiento del modelo de inteligencia artificial se realizará en futuras etapas del proyecto, considerando la predicción de la velocidad, temperatura, humedad y ubicación actual del ómnibus en tiempo real.
- Para garantizar la escalabilidad y la gestión efectiva de los datos, se ha seleccionado una única línea de ómnibus para la recolección inicial de datos.
