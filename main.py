import httpx
import asyncio
from datetime import datetime, timedelta
import schedule
import time

primer_ejecucion = True  

async def main():
    global primer_ejecucion  
    
    if primer_ejecucion:
        await obtener_datos()  
        primer_ejecucion = False  

    schedule.every(5).minutes.do(lambda: asyncio.run(obtener_datos()))

    while True:
        schedule.run_pending()
        time.sleep(1)

async def obtener_datos():
    hora_actual = datetime.now().time()
    hora_limite_inicio = datetime.strptime("00:06", "%H:%M").time()
    hora_limite_fin = datetime.strptime("06:43", "%H:%M").time()
    print(hora_actual)

    if hora_actual >= hora_limite_inicio and hora_actual >= hora_limite_fin:
        await obtener_datos_transporte()
        await obtener_datos_clima()
    else:
        print("Fuera del intervalo de tiempo permitido")


async def obtener_datos_transporte():
    token_url = "https://mvdapi-auth.montevideo.gub.uy/auth/realms/pci/protocol/openid-connect/token"
    client_id = "e131f1da"  
    client_secret = "4035ef34d9e934542d033485fa17bbe5"  

    token_params = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    async with httpx.AsyncClient() as client:
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
                print(api_response_transporte.json())
            else:
                print("Error al hacer la solicitud a la API de transporte público:", api_response_transporte.status_code)
        else:
            print("Error al obtener el token de acceso:", token_response.status_code)

async def obtener_datos_clima():
   

    url = f"https://api.open-meteo.com/v1/forecast?latitude=-32.5228&longitude=-55.7658&current=temperature_2m,relative_humidity_2m"    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

        if response.status_code == 200:
            datos_clima = response.json()
            temperatura = datos_clima["current"]["temperature_2m"]
            print(f"La temperatura en Uruguay es de {temperatura} grados Celsius.")
        else:
            print("Error al obtener datos meteorológicos:", response.status_code)

asyncio.run(main())
