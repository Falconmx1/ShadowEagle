import requests
from colorama import Fore, Style
import webbrowser
import os

def track_ip(save_history=None):
    ip = input(f"{Fore.CYAN}[+] Ingrese IP objetivo: {Style.RESET_ALL}")
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,lat,lon,isp,org,as,query", timeout=5)
        data = response.json()
        if data['status'] == 'success':
            result = f"IP: {data['query']}\nPaís: {data['country']}\nRegión: {data['regionName']}\nCiudad: {data['city']}\nISP: {data['isp']}\nCoordenadas: {data['lat']}, {data['lon']}"
            print(f"{Fore.GREEN}[+] {result}")
            if save_history:
                save_history(f"IP: {ip}", result)
            # Generar mapa con Leaflet
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Mapa - {ip}</title>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
                <style>#map {{ height: 400px; width: 100%; }}</style>
            </head>
            <body>
                <h3>Ubicación de {ip}</h3>
                <div id="map"></div>
                <script>
                    var map = L.map('map').setView([{data['lat']}, {data['lon']}], 13);
                    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{attribution: '© OpenStreetMap'}}).addTo(map);
                    L.marker([{data['lat']}, {data['lon']}]).addTo(map).bindPopup('{ip}<br>{data['city']}, {data['country']}');
                </script>
            </body>
            </html>
            """
            with open(f"exports/map_{ip}.html", "w") as f:
                f.write(html)
            print(f"{Fore.GREEN}[+] Mapa generado: exports/map_{ip}.html")
            webbrowser.open(f"exports/map_{ip}.html")
        else:
            print(f"{Fore.RED}[!] Error: {data.get('message', 'Desconocido')}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")
