#!/usr/bin/env python3
# ShadowEagle - OSINT Tool by HUNX

import os
import sys
import json
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from colorama import init, Fore, Style

init(autoreset=True)

# Importar módulos
from modules import (
    ip_tracker, username_tracker, email_breach, dns_lookup,
    mac_lookup, port_scanner, serial_tracker, image_reverse, batch_processor
)

BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
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
{Fore.GREEN}     [ 8 ] Escanear Puertos Abiertos
{Fore.GREEN}     [ 9 ] Tracking de Número de Serie (dispositivos)
{Fore.GREEN}     [10] Búsqueda Inversa de Imágenes
{Fore.GREEN}     [11] Modo Batch (archivo con múltiples IPs/usuarios)
{Fore.GREEN}     [12] Exportar resultados a PDF/CSV
{Fore.GREEN}     [13] Iniciar Interfaz Web (Flask + Mapas)
{Fore.GREEN}     [14] Historial de búsquedas
{Fore.RED}     [ 0 ] Exit
{Fore.YELLOW}═══════════════════════════════════════════════════════════════════
{Fore.CYAN} [ + ] Select Option : {Style.RESET_ALL}"""

HISTORY_FILE = "history/search_history.json"

def ensure_dirs():
    os.makedirs("exports", exist_ok=True)
    os.makedirs("history", exist_ok=True)

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(entry, result=""):
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "query": entry,
        "result": result[:200]  # Guardar primeros 200 caracteres
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

def export_to_pdf(data, filename):
    c = canvas.Canvas(f"exports/{filename}.pdf", pagesize=letter)
    c.drawString(100, 750, f"ShadowEagle Report - {datetime.now()}")
    y = 720
    for line in data.split('\n'):
        c.drawString(100, y, line[:100])
        y -= 20
    c.save()
    print(f"{Fore.GREEN}[+] PDF exportado: exports/{filename}.pdf")

def export_to_csv(data, filename):
    with open(f"exports/{filename}.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)
    print(f"{Fore.GREEN}[+] CSV exportado: exports/{filename}.csv")

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
        result = f"País: {country}\nOperador: {operator}\nZona: {', '.join(timezones)}"
        print(f"{Fore.GREEN}[+] {result}")
        save_history(f"Phone: {number}", result)
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}")

def export_menu():
    print(f"{Fore.YELLOW}[+] Exportar historial a:\n1. PDF\n2. CSV")
    opt = input("Opción: ")
    history = load_history()
    if not history:
        print(f"{Fore.RED}[!] No hay datos para exportar.")
        return
    if opt == '1':
        data = "\n".join([f"{h['timestamp']} - {h['query']}" for h in history])
        export_to_pdf(data, "shadoweagle_report")
    elif opt == '2':
        data = [[h['timestamp'], h['query'], h.get('result', '')] for h in history]
        export_to_csv(data, "shadoweagle_history")

def main():
    ensure_dirs()
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(BANNER)
        print(MENU)
        choice = input()
        if choice == '1':
            ip_tracker.track_ip(save_history)
        elif choice == '2':
            get_my_ip()
        elif choice == '3':
            phone_tracker()
        elif choice == '4':
            username_tracker.search_username(save_history)
        elif choice == '5':
            email_breach.check_breach(save_history)
        elif choice == '6':
            dns_lookup.query_dns(save_history)
        elif choice == '7':
            mac_lookup.lookup_mac(save_history)
        elif choice == '8':
            port_scanner.scanner(save_history)
        elif choice == '9':
            serial_tracker.track_serial(save_history)
        elif choice == '10':
            image_reverse.reverse_image_search(save_history)
        elif choice == '11':
            batch_processor.batch_process(save_history)
        elif choice == '12':
            export_menu()
        elif choice == '13':
            print(f"{Fore.GREEN}[+] Iniciando servidor web en http://localhost:5000")
            os.system("python web_app.py")
        elif choice == '14':
            show_history()
        elif choice == '0':
            print(f"{Fore.RED}[+] Saliendo...")
            sys.exit(0)
        else:
            print(f"{Fore.RED}[!] Opción inválida.")
        input(f"\n{Fore.YELLOW}[+] Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
