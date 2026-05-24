import os
from colorama import Fore
from modules import ip_tracker, username_tracker

def batch_process(save_history=None):
    file_path = input(f"{Fore.CYAN}[+] Ruta del archivo con IPs/usuarios (uno por línea): {Style.RESET_ALL}")
    if not os.path.exists(file_path):
        print(f"{Fore.RED}[!] Archivo no encontrado.")
        return
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    print(f"{Fore.GREEN}[+] Procesando {len(lines)} elementos...")
    for item in lines:
        print(f"{Fore.YELLOW}\n[+] Procesando: {item}")
        # Detectar si es IP o username
        if item.replace('.', '').isdigit() and len(item.split('.')) == 4:
            ip_tracker.track_ip(save_history)
        else:
            username_tracker.search_username(save_history)
