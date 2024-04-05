import httpx
import asyncio
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from enum import Enum
import locale

load_dotenv()

TRANSPORTE_CLIENT_ID = os.getenv("TRANSPORTE_CLIENT_ID")
TRANSPORTE_CLIENT_SECRET = os.getenv("TRANSPORTE_CLIENT_SECRET")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def dia_semana_actual():
    fecha_actual = datetime.today()
    dia_semana_numero = fecha_actual.weekday()
    return dia_semana_numero
async def obtener_datos():
    hora_actual = datetime.now().time()
    hora_limite_inicio = datetime.strptime("00:06", "%H:%M").time()
    hora_limite_fin = datetime.strptime("06:43", "%H:%M").time()
    print(hora_actual)

    if hora_limite_inicio <= hora_actual and hora_limite_fin <= hora_actual:
        
        datos_transporte = await obtener_datos_transporte()
        datos_clima = await obtener_datos_clima()
        print(datos_transporte) 
        print(datos_clima)
        hora_actual = datetime.now()
        hora_formateada = hora_actual.strftime("%H:%M:%S")
            
        if datos_transporte is not None and datos_clima is not None:
            velocidad = datos_transporte[0].get("speed", 0)
            velocidad1 = datos_transporte[1].get("speed", 0)
                
            data1 = {
                "VELOCIDAD": datos_transporte[0].get("speed", 0),
                "CORDENADAS": datos_transporte[0]["location"],
                "TEMPERATURA": int(datos_clima.get("temperatura", 0)),
                "hora": hora_formateada,
                "vel_viento": int(velocidad),
                "humedad": int(datos_clima["humedad"]),
                "lineVariantId": int(datos_transporte[0]["lineVariantId"]),
                "Day": dia_semana_actual()
                }
            data2 = {
                "VELOCIDAD": velocidad1,
                "CORDENADAS": datos_transporte[1]["location"],
                "hora": hora_formateada,
                "TEMPERATURA": int(datos_clima.get("temperatura", 0)),
                "vel_viento": int(float(datos_clima["vel_viento"])),
                "humedad": int(float(datos_clima["humedad"])),
                "lineVariantId": int(datos_transporte[1]["lineVariantId"]),
                "Day": dia_semana_actual()
                }
                
            supabase.table('Primera_iteracion').insert([data1, data2]).execute()
        else:
            print("Algunas de las peticiones de datos dio error, intentando nuevamente...")
            await asyncio.sleep(5)
            await obtener_datos()     
    else:
        print("Fuera del intervalo de tiempo permitido")

async def obtener_datos_transporte():
    token_url = "https://mvdapi-auth.montevideo.gub.uy/auth/realms/pci/protocol/openid-connect/token"
    client_id = TRANSPORTE_CLIENT_ID   
    client_secret = TRANSPORTE_CLIENT_SECRET 

    token_params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    async with httpx.AsyncClient() as client:
        try:
            token_response = await client.post(token_url, data=token_params)

            if token_response.status_code == 200:
                access_token = token_response.json()["access_token"]

                api_url_transporte = "https://api.montevideo.gub.uy/api/transportepublico/buses?lines=117"
                headers = {
                    "Authorization": "Bearer " + access_token
                }

                api_response_transporte = await client.get(api_url_transporte, headers=headers)

                if api_response_transporte.status_code == 200:
                
                    print("Respuesta de la API de transporte público:")
                    transporte_1 = {"speed" : api_response_transporte.json()[0].get("speed",0),"location" : api_response_transporte.json()[0]['location']['coordinates'], "lineVariantId" : api_response_transporte.json()[0]["lineVariantId"]}
                    transporte_2 = {"speed" : api_response_transporte.json()[1].get("speed",0),"location" : api_response_transporte.json()[1]['location']['coordinates'], "lineVariantId" : api_response_transporte.json()[1]["lineVariantId"]}
                    return [transporte_1, transporte_2]
                else:
                    print("Error al hacer la solicitud a la API de transporte público:", api_response_transporte.status_code)
            else:
                print("Error al obtener el token de acceso:", token_response.status_code)
        except Exception as e:
            print("Error al obtener datos de transporte:", e)

async def obtener_datos_clima():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-34.90&longitude=-56.18&current=temperature_2m,wind_speed_10m,relative_humidity_2m"    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)

            if response.status_code == 200:
                datos_clima = response.json()
                variables_clima = {
                    "temperatura" : datos_clima["current"]["temperature_2m"],
                    "vel_viento" : datos_clima["current"]["wind_speed_10m"],
                    "humedad" : datos_clima["current"]["relative_humidity_2m"]
                }
                return variables_clima
            else:
                print("Error al obtener datos meteorológicos:", response.status_code)
        except Exception as e:
            print("Error al obtener datos meteorológicos:", e)

async def main():
    while True:
        await obtener_datos()
        await asyncio.sleep(30)

if __name__ == "__main__":     
    asyncio.run(main())


