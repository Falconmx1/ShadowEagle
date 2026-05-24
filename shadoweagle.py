#!/usr/bin/env python3
# ShadowEagle - OSINT Tool by HUNX

import os
import sys
import json
from datetime import datetime
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from colorama import init, Fore, Style

init(autoreset=True)

# Módulos personalizados (los crearemos después)
try:
    from modules import ip_tracker, username_tracker, email_breach, dns_lookup, mac_lookup, port_scanner
except ImportError as e:
    print(f"{Fore.RED}[!] Error importando módulos: {e}")
    print(f"{Fore.YELLOW}[!] Asegúrate de tener todos los archivos en la carpeta 'modules/'")

BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║       ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗       ║
║       ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔════╝ ██║    ██║       ║
║       ███████╗███████║███████║██║  ██║██║  ███╗██║ █╗ ██║       ║
║       ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║       ║
║       ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝       ║
║       ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝        ║
║           [ + ]  C O D E   B Y  H U N X  [ + ]                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

MENU = f"""
{Fore.YELLOW}═══════════════════════════════════════════════════════════════════
{Fore.GREEN}     [ 1 ] IP Tracker + Geolocalización precisa
{Fore.GREEN}     [ 2 ] Mostrar Mi IP Pública
{Fore.GREEN}     [ 3 ] Phone Number Tracker + Operador
{Fore.GREEN}     [ 4 ] Username Tracker en 300+ redes
{Fore.GREEN}     [ 5 ] Email Breach Check (HaveIBeenPwned)
{Fore.GREEN}     [ 6 ] DNS Lookup + WHOIS
{Fore.GREEN}     [ 7 ] MAC Address Vendor Lookup
{Fore.GREEN}     [ 8 ] Escanear Puertos Abiertos (IP Objetivo)
{Fore.GREEN}     [ 9 ] Historial de búsquedas
{Fore.RED}     [ 0 ] Exit
{Fore.YELLOW}═══════════════════════════════════════════════════════════════════
{Fore.CYAN} [ + ] Select Option : {Style.RESET_ALL}"""

HISTORY_FILE = "search_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(entry):
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": entry
    })
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def show_history():
    history = load_history()
    if not history:
        print(f"{Fore.RED}[!] No hay historial aún.")
        return
    print(f"{Fore.CYAN}\n[+] Historial de búsquedas:\n")
    for i, entry in enumerate(history, 1):
        print(f"{Fore.YELLOW}[{i}] {entry['timestamp']} -> {entry['query']}")

def get_my_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        ip = response.json()['ip']
        print(f"{Fore.GREEN}[+] Tu IP pública es: {Fore.CYAN}{ip}")
        save_history(f"Mi IP: {ip}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error obteniendo IP: {e}")

def phone_tracker():
    number = input(f"{Fore.CYAN}[+] Ingrese número con código país (ej: +521234567890): {Style.RESET_ALL}")
    try:
        parsed = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(parsed):
            print(f"{Fore.RED}[!] Número inválido.")
            return
        country = geocoder.description_for_number(parsed, "es")
        operator = carrier.name_for_number(parsed, "es")
        timezones = timezone.time_zones_for_number(parsed)
        print(f"{Fore.GREEN}[+] País: {Fore.CYAN}{country}")
        print(f"{Fore.GREEN}[+] Operador: {Fore.CYAN}{operator}")
        print(f"{Fore.GREEN}[+] Zona horaria: {Fore.CYAN}{', '.join(timezones)}")
        save_history(f"Phone: {number}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")

def main():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(BANNER)
        print(MENU)
        choice = input()
        if choice == '1':
            ip_tracker.track_ip()
        elif choice == '2':
            get_my_ip()
        elif choice == '3':
            phone_tracker()
        elif choice == '4':
            username_tracker.search_username()
        elif choice == '5':
            email_breach.check_breach()
        elif choice == '6':
            dns_lookup.query_dns()
        elif choice == '7':
            mac_lookup.lookup_mac()
        elif choice == '8':
            port_scanner.scanner()
        elif choice == '9':
            show_history()
        elif choice == '0':
            print(f"{Fore.RED}[+] Saliendo...")
            sys.exit(0)
        else:
            print(f"{Fore.RED}[!] Opción inválida.")
        input(f"\n{Fore.YELLOW}[+] Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
