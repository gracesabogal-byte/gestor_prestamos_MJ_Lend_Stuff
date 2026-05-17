"""
pf_Algoritmos
Gestor de Prestamos - MJ Lend-Stuff
Proyecto Integrador Algoritmia y Programacion 2026-1
Universidad de Antioquia - Ingenieria Industrial
"""

import os
import sys
from menu import mostrar_menu_principal

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_banner():
    limpiar_pantalla()
    print("=" * 70)
    print("""
  __  __ _       _                  _   ____  _         __  __ 
 |  \/  | |     | |                | | / ___|| |_ _   _ / _|/ _|
 | |\/| | |     | |     ___ _ __  __| | \___ \| __| | | | |_| |_ 
 | |  | | |___  | |___ / _ \ '_ \/ _` |  ___) | |_| |_| |  _|  _|
 |_|  |_|_____| |_____|\___/_| |_\__,_| |____/ \__|\__,_|_| |_|  
    """)
    print("          Bienvenido a MJ Lend-Stuff - Gestor de Prestamos")
    print("=" * 70)

if __name__ == "__main__":
    mostrar_banner()
    mostrar_menu_principal()
