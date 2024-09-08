import requests
import re
import time
from tqdm import tqdm
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Validación de IP
def is_valid_ip(ip):
    pattern = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    if pattern.match(ip):
        return all(0 <= int(octet) <= 255 for octet in ip.split('.'))
    return False

# Obtener la ubicación a partir de una IP con ip-api.com
def get_location_by_ip(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=5)
    except requests.Timeout:
        return f"{Fore.RED}Error: Tiempo de espera agotado para obtener la información."
    except requests.ConnectionError:
        return f"{Fore.RED}Error: No se pudo conectar con el servicio de geolocalización."
    except requests.RequestException:
        return f"{Fore.RED}Error: Ocurrió un problema inesperado al intentar obtener la información."

    # Si el estado HTTP no es 200, reportamos el error
    if response.status_code != 200:
        return f"{Fore.RED}Error: La API devolvió un código de estado {response.status_code}."

    data = response.json()
    status = data.get("status", "fail")
    
    if status == "success":
        city = data.get("city", "No disponible")
        region = data.get("regionName", "No disponible")
        country = data.get("country", "No disponible")
        isp = data.get("isp", "No disponible")
        lat = data.get("lat", None)
        lon = data.get("lon", None)
        
        # Crear un enlace de Google Maps si tenemos las coordenadas
        if lat and lon:
            map_url = f"https://www.google.com/maps?q={lat},{lon}"
        else:
            map_url = "No disponible"

        result = f"""
        {Fore.CYAN}Información de la IP {ip}:{Style.RESET_ALL}
        {Fore.GREEN}Ciudad: {city}
        Región: {region}
        País: {country}
        Proveedor: {isp}
        Latitud: {lat}
        Longitud: {lon}
        {Fore.YELLOW}Enlace a Google Maps: {map_url}{Style.RESET_ALL}
        """
        return result
    else:
        return f"{Fore.RED}Error: No se pudo obtener información para la IP {ip}"

# Barra de progreso
def show_progress():
    for _ in tqdm(range(50), desc="Obteniendo información", ascii=False, ncols=75):
        time.sleep(0.05)

# Función principal
def main():
    print(f"{Fore.BLUE}Bienvenido al Localizador de IP en Tiempo Real\n{Style.RESET_ALL}")

    while True:
        ip = input("Por favor ingresa la dirección IP (o escribe 'salir' para terminar): ")

        if ip.lower() == 'salir':
            print(f"{Fore.YELLOW}Saliendo del programa...{Style.RESET_ALL}")
            break

        if not is_valid_ip(ip):
            print(f"{Fore.RED}Error: La dirección IP {ip} no es válida. Intenta de nuevo.{Style.RESET_ALL}")
            continue

        # Mostrar barra de progreso para simular "tiempo real"
        show_progress()

        # Mostrar la información de la IP con el enlace de Google Maps
        print(get_location_by_ip(ip))

if __name__ == "__main__":
    main()